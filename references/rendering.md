# 精确排字接口

运行 `python3 scripts/render_cover.py --recipe recipe.json`。需要 Pillow 和 fontTools；依赖参见 requirements-render.txt。配方路径内的相对路径相对于配方文件所在目录：

```json
{"format":"feishu","image":"base.png","output":"cover.png","typography":"editorial","title":"上下文的边界","subtitle":"The Shape of Context","color":"#2148B8","anchor":[0.5,0.5],"text_box":[710,80,1290,320]}
```

只把无字底图送入渲染器；仅以等比居中裁切适配画幅。必须预先构图，确保裁切后主体仍可辨；成品必须人工检查。脚本自动校验文字、字形覆盖、行宽、安全区及输出尺寸；标题过长时报错，不删改、拉伸或自动编造文字。中英文分别使用配套真实字体；生成器命名字体不代表实际加载了字体。

`text_box` 可选，单位为目标像素，必须位于安全区内。默认使用整个安全区；`align` 可选 left、center 或 right。anchor 是等比裁切的水平和垂直位置，范围均为 0–1。混排标题目前使用中文主字体中的拉丁字形；需要字族完全分离时应分层排版。

可选 `foreground` 指向与画布等大的透明 PNG；前景层覆盖字形笔画时拒绝输出。请使用图像生成工具制作前景，且人工核验视觉效果。
