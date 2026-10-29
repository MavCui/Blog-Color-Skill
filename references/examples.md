# 用法与样例

## 请求

- “用 $editorial-wide-cover 为这篇Agent文章做飞书顶部封面，标题‘协作的另一端’。”
- “同篇文章做飞书5:1与社交2.35:1两个版式，保留同一隐喻。”
- “只用中文，‘判断的尺度’，黑红，宋体有力量，16:9。”
- “沿用主系列油墨，为这六篇文章各选不同物件，先出前三张。”
- “严格用真实思源宋体、Bodoni Moda排字，先生成无字底图。”

## 首轮方向样例

**上下文的边界 / The Shape of Context**：蓝橙，中性白，editorial。一只巨大线轴，从缠绕中抽出单根橙线；中央图字紧锁，线向两翼延伸。线刻工艺。表达选择保留与释放。

**协作的另一端 / The Other End**：绿酒红，中性白，literary。大小悬殊的滑轮共用一根线，酒红只突出小轮；尺度关系表达协作和借力。社交宽屏。

**判断的尺度 / A Measure of Judgment**：黑红，冷灰，critical。巨大筛网裁出边缘，一枚红物件被留住，小黑碎屑落下；标题切入轮廓。16:9。

这些不是每次固定复用的模板。首轮编号仅为样图标识，不把它变成所有输出的虚构期号。

## 可查看的真实生成样图

- [A：蓝橙线轴](../assets/examples/A-context.png)，1983×793，原生审美预览，未达到飞书5:1。
- [B：绿酒红滑轮](../assets/examples/B-collaboration.png)，1922×818，约2.35:1原生社交宽屏预览。
- [C：黑红筛网](../assets/examples/C-judgment.png)，1672×941，约16:9原生社交预览。

样图展示物件关系、裁切和模型绘制衬线字形；不代表真实字体文件排字或所有规格检查已通过。需要模仿这一系列气质时先查看图片，只提取视觉语法，不照抄题目和物件。

## Prompt结构

开头：Create an ORIGINAL flat landscape editorial cover for a personal publication. Contemporary art-book publishing, a concrete object metaphor and one arresting visual relation. [Exact ratio/dimensions/paper/inks].

中间：写出本篇可见物件、尺度、裁切、安全区、准确标题与字体特征。

结尾：Render only the quoted text verbatim. Keep Chinese Song/Ming serif strokes crisp; [chosen English serif anatomy]. Exactly two inks and exposed paper. No mockup, technology stock imagery, glossy 3D, gradient, extra words, watermark or invented brand.

## 纠错

错字只改错字，保留构图；一次仍失败走无字底图。普通构图只增强一个尺度或裁切动作，不同时堆网格、手写、拼贴。比例问题按formats.md处理。中文像黑体则补充三角衬线、粗竖细横，减少字上颗粒。系列太像则换物件关系与主视觉动作，不仅移动标题。
