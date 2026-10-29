#!/usr/bin/env python3
"""Render a text-free image with exact bundled fonts; output requires visual QA."""
import argparse, json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]

def load_font(spec, size, text):
    path = ROOT / 'assets/fonts' / spec['file']
    if not path.is_file():
        raise ValueError('Missing font: ' + str(path))
    tt = TTFont(path, lazy=True)
    cmap = tt.getBestCmap()
    missing = sorted({c for c in text if not c.isspace() and ord(c) not in cmap})
    if missing:
        raise ValueError('Font missing glyphs: ' + ''.join(missing))
    axes = []
    if 'fvar' in tt:
        for a in tt['fvar'].axes:
            axes.append(max(a.minValue, min(a.maxValue, spec.get('weight', a.defaultValue))) if a.axisTag == 'wght' else a.defaultValue)
    tt.close()
    font = ImageFont.truetype(str(path), size)
    if axes:
        font.set_variation_by_axes(axes)
    return font

def fit_lines(text, font, max_width, draw):
    lines = []
    for paragraph in text.split('\n'):
        if not paragraph:
            lines.append(''); continue
        words = paragraph.split(' ') if ' ' in paragraph else list(paragraph)
        sep = ' ' if ' ' in paragraph else ''
        line = ''
        for word in words:
            candidate = line + (sep if line else '') + word
            if draw.textlength(candidate, font=font) > max_width:
                if not line: raise ValueError('A word does not fit the safe area')
                lines.append(line); line = word
            else: line = candidate
        lines.append(line)
    return lines

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--recipe',required=True,type=Path)
    a=parser.parse_args(); recipe=json.loads(a.recipe.read_text(encoding='utf-8')); base=a.recipe.resolve().parent
    presets=json.loads((ROOT/'references/presets.json').read_text()); fmt=presets['formats'][recipe['format']]; pair=presets['typography'][recipe.get('typography','editorial')]
    title=recipe['title']; subtitle=recipe.get('subtitle','')
    if not title.strip(): raise ValueError('Title is empty')
    source=(base/recipe['image']).resolve(); output=(base/recipe['output']).resolve()
    if output.exists(): raise ValueError('Output already exists; choose a new filename')
    if source==output: raise ValueError('Output cannot replace the source')
    anchor=recipe.get('anchor',[0.5,0.5])
    if len(anchor)!=2 or any(not 0<=v<=1 for v in anchor): raise ValueError('Anchor values must be in 0–1')
    im=Image.open(source).convert('RGB'); w,h=fmt['size']; im=ImageOps.fit(im,(w,h),method=Image.Resampling.LANCZOS,centering=tuple(anchor))
    draw=ImageDraw.Draw(im); sx1,sy1,sx2,sy2=fmt['safe_rect']
    x1,y1,x2,y2=recipe.get('text_box',fmt['safe_rect'])
    if not (sx1 <= x1 < x2 <= sx2 and sy1 <= y1 < y2 <= sy2):
        raise ValueError('Text box must be inside the safe area')
    width=x2-x1; height=y2-y1
    title_size=int(recipe.get('title_size', min(150,round(h*.16)))); min_size=int(recipe.get('min_title_size',max(24,round(h*.1))))
    sub_size=int(recipe.get('subtitle_size',max(20,round(title_size*.42))))
    if not (0 < min_size <= title_size and sub_size>0): raise ValueError('Invalid font sizes')
    title_spec = pair['zh'] if any('\u3400' <= c <= '\u9fff' for c in title) else pair['en']
    subtitle_spec = pair['zh'] if any('\u3400' <= c <= '\u9fff' for c in subtitle) else pair['en']
    subfont=load_font(subtitle_spec,sub_size,subtitle) if subtitle else None
    sublines=fit_lines(subtitle,subfont,width,draw) if subtitle else []
    for size in range(title_size,min_size-1,-1):
        font=load_font(title_spec,size,title); lines=fit_lines(title,font,width,draw)
        line_height=round(size*1.25); sub_height=round(sub_size*1.3)
        total=len(lines)*line_height+(round(size*.15)+len(sublines)*sub_height if subtitle else 0)
        if total <= height: break
    else: raise ValueError('Title and subtitle do not fit; choose another layout or a shorter approved title')
    align=recipe.get('align','left')
    if align not in ('left','center','right'): raise ValueError('Invalid alignment')
    color=recipe.get('color','#30343A'); y=y1+(height-total)//2
    boxes=[]
    text_mask=Image.new('L',(w,h)); mask_draw=ImageDraw.Draw(text_mask)
    for text,f,step in [(line,font,line_height) for line in lines]+[(line,subfont,sub_height) for line in sublines]:
        if f is subfont and subtitle and y < y1+(height-total)//2+len(lines)*line_height+round(size*.15): y+=round(size*.15)
        tw=draw.textlength(text,font=f); x=x1 if align=='left' else x2-tw if align=='right' else x1+(width-tw)/2
        bbox=draw.textbbox((x,y),text,font=f,anchor='lt');
        if bbox[0]<x1 or bbox[1]<y1 or bbox[2]>x2 or bbox[3]>y2: raise ValueError('Text exceeds safe area')
        draw.text((x,y),text,font=f,fill=color,anchor='lt'); mask_draw.text((x,y),text,font=f,fill=255,anchor='lt'); boxes.append(bbox);y+=step
    if recipe.get('foreground'):
        layer=Image.open((base/recipe['foreground']).resolve()).convert('RGBA')
        if layer.size != (w,h): raise ValueError('Foreground must match the exact canvas size')
        if ImageChops.multiply(text_mask,layer.getchannel('A')).getbbox():
            raise ValueError('Foreground overlaps title strokes; revise the layout')
        im=Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
    output.parent.mkdir(parents=True,exist_ok=True); im.save(output,'PNG')
    print(json.dumps({'output':str(output),'size':[w,h],'title_lines':lines,'font_files':[title_spec['file'],subtitle_spec['file'] if subtitle else None],'text_bounds':boxes,'visual_qa':'required'},ensure_ascii=False))

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,OSError,TypeError) as e:
        print('Error: '+str(e),file=sys.stderr);sys.exit(1)
