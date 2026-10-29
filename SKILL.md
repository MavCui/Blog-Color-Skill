---
name: editorial-wide-cover
description: 为飞书文档顶部封面和社交媒体横屏文章封面生成原创艺术编辑视觉，使用预设中英衬线字体、受控双色印刷、物件隐喻与裁切构图。适用于文章系列封面、知识栏目头图、横屏 zine/editorial cover；普通竖版海报、UI 和信息图不使用。
---

# Blog Color · 纸上思考

把 AI、技术、产品、工作方法或其他文章主题，转成有停留感的原创艺术出版物封面。默认生成真实位图，不以文字方案或 SVG 代替生图。明确要求分析、只写 prompt 或先做规范时，尊重该范围。

## 读取资源

- 生成前读取 [视觉规则](references/art-direction.md)、[中英字体](references/typography.md) 与 [画幅及安全区](references/formats.md)。
- 精确参数使用 [presets.json](references/presets.json)。批量样图参考 [examples.md](references/examples.md)，不要固定复用其中的物件。
- 用户追溯来源或更新规格时读取 [sources.md](references/sources.md)。普通生成不用重复联网研究。

## 默认选择

| 参数 | 默认 |
|---|---|
| 载体 | 飞书文档：feishu；其他未点名平台的横屏：social-wide |
| 配色 | cobalt-terracotta：钴蓝与陶土橙 |
| 纸面 | 中性白 #FAFAF7，轻微纸纹，无泛黄 |
| 字体 | editorial：思源宋体 SC SemiBold＋Bodoni Moda Medium |
| 主体 | 一个具体物件或两个存在明确关系的物件 |
| 构图 | 一个主视觉事件＋一片安静纸面，图字相交但文字完整 |
| 文字 | 中文主导；短英文副题可选，不强加双语 |
| 数量 | 未指定时一张；“一些样图”三张独立图片 |

本系列中英标题均为衬线，不因技术主题自动改成黑体、终端字。等宽字只用于很小的可选期号。用户明确要求优先于默认。

## 工作流

1. 提炼文章的一种关系，如筛选、遗忘、连接、委托、摩擦、反馈、边界。选择一个能使该关系可见的具体物件或动作，而非画整篇文章目录。
2. 确定准确短题、可选副题、用户提供的栏目名或期号。提供的文字逐字保留。长题放不下时，为样稿拟一个忠实短题并标明；不擅自更改原文章标题。
3. 解析载体、目标尺寸、安全区、字体、两种油墨。系列保持配色与字体；比较方向或用户要求变化时再换配色。
4. 选一个主动作：巨大裁切、异常尺度、集中叠印、纸面切穿或文字物件。其他动作退为支持，不同时形成多个焦点。
5. 按下方结构编译实际 prompt，调用可用的内置图像生成工具。每张独立调用；不把联系表冒充独立成品。使用可用的 imagegen skill 处理工具参数、输入图与保存策略。
6. 查看真实输出：逐字检查、读取实际尺寸、检查中央安全区与缩略图。字体名是视觉指令，不等于模型精确载入字体文件。
7. 明显错误时针对失败点修正一次，保持主题、准确文字及选定系统。仍有局限则交付可用样稿并如实标注，不无限生成。

## Prompt 结构

用简洁英文描述可见画面，中文准确文字用引号包住。不把内部 ID 当作画面元素。

```text
Use case: stylized-concept.
Asset: original flat landscape editorial article cover, [ratio and dimensions].
Paper and inks: [substrate hex], exactly [inks and hex], [plate roles].
Subject: [one concrete object and visible relationship expressing the article].
Composition: [one focal event, crop, quiet region, image-type interaction].
Keep [safe rectangle] for all essential wording and recognition anchors.
Typography: [Chinese family/weight AND visible Song/Ming anatomy];
[English serif family/weight/style AND visible anatomy]. [Hierarchy/line breaks].
Text verbatim: "[Chinese]"; optionally "[English]"; optionally "[provided issue]".
Print: [one primary process], exposed paper, [zero or one subtle imperfection].
Avoid: [relevant short negative list]. No additional words.
```

必须包含比例、安全区、准确文案、中英字体特征、图字位置关系。不能只写“高端、艺术、极简、杂志感”。

## 系列与多比例

- 跨平台保留隐喻、油墨、纸面、字体及识别核心，按比例重新排版。禁止将 16:9 拉成 5:1。
- 飞书先解决中央信息核心，再向两翼延伸可裁片段。安全区居中不等于全部元素居中对称。
- 社交版可以释放物件尺度与标题大小，不照搬飞书窄小信息簇。
- 相邻封面改变物件结构与主视觉动作。稳定来自油墨、字体、纸面及信息纪律，不来自永远“左标题右物件”。
- 同题比较三种方向时控制文案、主题及画幅；展示能力范围时才组合不同主题与画幅，并标明用途。

## 字体和文字可靠性

真实字体、授权与来源哈希在 assets/fonts/。生图 prompt 不会自动加载这些字体。

- 默认：模型绘制文字，检查准确性与衬线外观；称为“按预设风格生成”，不声称使用精确字体文件。
- 用户要求真实字体一致，或中文修正一次仍不可靠：生成无字底图并预留排版区，使用可用排版工具实际加载随附字体、保留文字层后导出。工具做不到时交付底图及规格，不伪称已经排好。
- 已有位图改字、裁切、重构画幅，遵循当前图像工具的编辑规则；不用代码绕过工具限制重绘图像。
- 不将缺字、乱码、错误偏旁视为完成；也不在图片仍错时只把正确文字写进说明冒充修复。

## 交付检查

- 主题隐喻可读，无科技套图；缩略图有一个形态事件和安静区域。
- 最多两墨，各有职责；纸面不算墨；不加入黑色第三墨。
- 中文、英文标题符合衬线体系，细横画未被颗粒破坏。
- 文案逐字正确，无假品牌、假日期与装饰性乱码。
- 飞书关键文字与识别锚点在中央安全区，两翼可裁掉。
- 实际读取尺寸和大小，按 formats.md 区分原生样图与成品。可运行 `python3 scripts/inspect_cover.py PATH --preset feishu`；该脚本只查文件几何，不证明文字或视觉安全。

## 输出

先图片，再用一两句说明方向、用途与实际局限。多图标 A/B/C，并给简短推荐。先看样图时不要在聊天贴大段规范。

保存图片、完整实际 prompt 和小型 recipe JSON，记录准确文案、字体/配色预设、目标/实际尺寸、QA状态。默认目录为当前工作区 output/editorial-wide-cover/<date>/，避免覆盖。回复链接实际 prompt 文件，用户要求时再展开全文。

只有尺寸、裁切与文字检查通过才称为“可直接上传飞书的封面”。发布或写入外部应用不属于默认范围。
