# 中英衬线字体

## 随附资源

assets/fonts/ 包含原版字体与OFL授权。真实排字时直接加载，不需要系统级安装。模型不会仅通过prompt自动加载文件。

| 角色 | 字体 | 字形与分工 |
|---|---|---|
| 中文主标题 | Source Han Serif SC SemiBold／思源宋体SC半粗 | 方整结构、三角衬线、粗竖细横、清晰的出版物气质 |
| 英文主副题 | Bodoni Moda，500–600 | 高反差现代衬线、精细hairline serif、光学校正间距 |
| 柔和英文副题 | Cormorant Garamond，500–600 | 古典曲线、bracketed serif、可用短斜体 |
| 可选期号 | IBM Plex Mono Regular | 只用于用户给定的小期号，不作标题 |

## 三个预设

- **editorial**：中文思源宋体半粗＋英文Bodoni Moda Medium 500，roman默认，短随笔副题可italic。主系列用此组合。
- **literary**：中文思源宋体半粗，以较宽松行距和温和尺度调整；英文Cormorant Garamond Medium 500–600，可用italic。适合人文关系。
- **critical**：中文思源宋体半粗，放大字号、收紧行距，以尺度增强力度，不伪粗；英文Bodoni Moda SemiBold 600正体。适合判断与观点。

## 模型字形描述

中文同时给字体名与可见特征：

> Refined Chinese Song/Ming serif, triangular wedge serifs, strong vertical strokes, elegant thin horizontal strokes, crisp square CJK structure, no brush calligraphy and no sans-serif substitution.

英文按所选字体写：Bodoni用“high-contrast editorial serif, sculpted thick/thin strokes, fine hairline serifs”；Cormorant用“old-style editorial serif, graceful curves, delicately bracketed serifs”。不要两种混写。不要过度奢侈品logo式字距。

## 排版起点

| 最终画布 | 中文主题 | 英文副题 | 可选期号 |
|---|---|---|---|
| 飞书2000×400 | 44–68px | 22–30px | 14–18px |
| 社交2350×1000 | 110–160px | 42–64px | 22–30px |
| 通用1920×1080 | 100–150px | 40–58px | 20–28px |

这些是起点，必须共同装入安全区。中文短题优先4–8字，一到两行；单行不够先断行，不压扁字形。英文副题优先2–6词，可省略。中文主导时，英文视觉高度约中文35%–50%。用户未给期号不要编造日期与栏目编号。

中文字距约-0.02em至0.04em，按具体字形光学校正；行距按字框和叠图调整。中英混排按视觉基线，不强求数学等高。图字叠合可做纸面镂空，不切掉中文识别笔画。飞书安全区内主标题完整。

小字Bodoni用较低optical size约12–24及适中字重；大标题再提高。标题保持实墨，颗粒主要处理图像。不要以极细极小字假装高级，不用手写/花体/黑字哥特作默认标题。

## 精确排字

模型文字只能检查准确性和外观，不能声称实际用了精确font family。用户要求字体一致或错字修正一次仍失败，改成无字底图＋真实排字：加载随附文件、保留可编辑文字层、检查导出。当前工具做不到则交付底图与规格，并说明待排字。

只有半粗中文静态字重已随附。需其他真实字重从官方补充并保留许可，不用描边拉伸伪造。用户接受系统替代时可用Songti SC、Bodoni 72或Baskerville，需说明替代；不要打包系统商业字体。
