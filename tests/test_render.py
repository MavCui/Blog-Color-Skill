import json, subprocess, sys, tempfile, unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts/render_cover.py'
class RenderTest(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.p=Path(self.t.name)
  Image.new('RGB',(1200,700),'white').save(self.p/'base.png')
 def tearDown(self):self.t.cleanup()
 def run_recipe(self,**kw):
  r={'format':'feishu','image':'base.png','output':'result.png','typography':'editorial','title':'上下文的边界','subtitle':'The Shape of Context'};r.update(kw)
  (self.p/'recipe.json').write_text(json.dumps(r,ensure_ascii=False))
  return subprocess.run([sys.executable,str(SCRIPT),'--recipe',str(self.p/'recipe.json')],capture_output=True,text=True)
 def test_feishu_exact(self):
  r=self.run_recipe();self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(Image.open(self.p/'result.png').size,(2000,400));self.assertEqual(json.loads(r.stdout)['title_lines'],['上下文的边界'])
 def test_swiss_chinese(self):
  r=self.run_recipe(typography='swiss',title='结构与秩序',subtitle='Structure');self.assertEqual(r.returncode,0,r.stderr)
 def test_english_title_uses_latin_font(self):
  r=self.run_recipe(title='A Measure of Context');self.assertEqual(r.returncode,0,r.stderr);self.assertIn('BodoniModa',json.loads(r.stdout)['font_files'][0])
 def test_long_title_fails(self):
  r=self.run_recipe(title='上下文的边界'*100);self.assertNotEqual(r.returncode,0);self.assertFalse((self.p/'result.png').exists())
 def test_missing_glyph_fails(self):
  r=self.run_recipe(title='上下文 🦄');self.assertNotEqual(r.returncode,0);self.assertFalse((self.p/'result.png').exists())
 def test_no_overwrite(self):
  (self.p/'result.png').write_bytes(b'preserve');r=self.run_recipe();self.assertNotEqual(r.returncode,0);self.assertEqual((self.p/'result.png').read_bytes(),b'preserve')
if __name__=='__main__':unittest.main()
