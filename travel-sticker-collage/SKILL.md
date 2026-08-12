---
name: travel-sticker-collage
description: "从至少 2 张上传照片中识别共同主题或提炼松散照片的视觉共性，以独立语义对象抠图为主要单位，提取主体、物件、纹理和少量环境片段，并依据本组素材的主色、主题气质与 hero 对比自动选择背景色，生成彩色贴纸杂志风的无文字拼贴海报；适用于旅行、活动、展览、日常和随机照片组，支持任意张数。"
---

# 彩色贴纸旅行拼贴

## 目标

把照片组转成一张竖版 4:5、无新增文字的彩色贴纸杂志海报。使用明快但受控的高对比配色、干净主体抠图、轻微贴纸描边、纯色纸片和少量半调网点。

不要依赖固定风格参考图。只根据用户素材、主题分析和本 Skill 的提示词规则建立视觉效果，避免参考图把背景色、构图和对象类型锁死。

## 不可妥协的视觉约束

### 1. 以独立语义对象为基本单位

- 默认把每个前景元素沿真实语义轮廓抠出，移除原照片背景；目标是至少 80% 的摄影元素按数量呈现为独立对象或语义对象组。
- 允许保留语义上完整的对象组，例如一套餐盘、花束、一只手握着一组卡牌、人物连同所坐的椅子。对象组的外轮廓仍须被抠出。
- 不允许把餐桌、房间、街道、广场或整张风景照片当成前景对象。餐盘可以保留，整张餐桌照片不可以；地标建筑可以抠出，整片城市画面不可以。
- 给独立对象使用平滑、准确的轮廓，可加细窄奶油白描边和轻微错位阴影。不要给对象外围制造粗糙撕裂照片边缘。

### 2. 严格限制完整环境照片

- 每张海报最多指定 1 张照片为 `ENVIRONMENT_ANCHOR`，用作海滩、海面、天空、城市地平线等大环境层。
- 环境锚点最多占画布约 30%，放在下部、后部或一个明确的有机窗口内，不与 hero 争夺视觉中心。
- 最多再使用 1 个小型环境窗口，面积不超过画布约 8%，只允许圆形、窄条或整齐有机 mask。
- 其他风景照片必须提取具体对象，例如建筑、树、船、车辆、动物、岩石、风机、桥或人物；若没有可抠主体，只使用一条窄纹理、天空色块或小圆形局部。
- 禁止多个大型风景块、多个完整场景或连续撕裂照片彼此拼接成照片墙。

### 3. 把撕纸效果留给图形衬底

- 撕纸、网点、胶带和色块只用于非摄影的纯色纸片或抽象纹理衬底。
- 照片元素使用主体轮廓、圆形 crop、干净有机 mask 或单一环境锚点；不要给完整照片套撕裂边框。
- 禁止“整张照片 + 不规则撕边”的默认处理。禁止用大量撕裂矩形、撕裂竖条或拼图状完整场景填满画布。

## 输入规则

- 至少需要 2 张照片。少于 2 张时，请用户补充，不要用虚构素材填充。
- 不设照片数量上限。检查所有照片，并让每张至少贡献一个可辨识对象、语义对象组、颜色、纹理或环境局部。
- 主题明确时围绕共同地点或活动建立视觉叙事；主题松散时提炼颜色、形状、光线、材质和动作方向，做成视觉日记，不强行编造地点和故事。
- 不把原图排成九宫格、照片墙、等尺寸缩略图或撕纸场景集合。

## 工作流

### 1. 盘点照片并分类

逐张记录主主体、次主体、图案/材质、环境局部、主色和需要去除的文字。为每张照片的贡献指定以下类型之一：

- `OBJECT_CUTOUT`：单个独立主体，默认首选；
- `SEMANTIC_CLUSTER`：外轮廓完整的一组相关对象；
- `ENVIRONMENT_ANCHOR`：全组最多 1 张；
- `MICRO_TEXTURE`：小圆窗、窄条、图案或局部放大。

不要使用 `FULL_PHOTO_PATCH`。若初步计划中出现第二张大环境照片，立即改为提取其中的具体对象或微型局部。

### 2. 提取多样元素

优先从每张照片寻找不同类型的信息：

1. 主体剪影：动物、人物、雕塑、食物、商品或地标；
2. 支撑物件：容器、鞋、交通工具、椅子、卡牌、餐具等；
3. 图案与材质：布料、包装色块、砖墙、海水、沙滩、纸张；
4. 环境锚点：仅选择全组最有空间感的一张；
5. 细节放大：眼睛、蝴蝶结、鱼群、食物纹理、泡沫或局部图形。

可旋转、镜像、缩放、透视修正或局部放大，但保持对象可辨认。不要复制同一对象制造假数量；同一照片的多个裁切必须表达不同信息。

### 3. 按照片数量控制密度

| 照片数量 | 每张照片的目标贡献 | 构图策略 |
|---|---:|---|
| 2 张 | 3–5 个元素 | 每张提取主主体、次物件、纹理和局部细节；最多一张承担环境锚点 |
| 3–5 张 | 2–3 个元素 | 每张至少一个独立对象，再用微型纹理补足丰富度 |
| 6–12 张 | 1–2 个独立对象，另加少量细节 | 设置 1 个 hero、2–4 个 secondary，其余作为小型贴纸锚点 |
| 13 张以上 | 每张至少 1 个辨识贡献 | 相近对象组成节奏或小型群组，风景转为具体地标或微型窗口，不做场景墙 |

照片少时从每张多取几种对象；照片多时合并同类小对象。始终保持“丰富但一眼有重点”。

### 4. 组织构图

- 使用 1 个最大 hero、2–4 个 secondary 和 4–12 个 supporting/micro elements。
- 让 hero 和 secondary 都是独立抠图对象，不使用完整场景承担 hero。
- 用斜向动线、错位叠压和比例反差连接对象；让独立对象轻微覆盖纯色衬底和环境锚点。
- 保留明确外边距与局部留白。对象可以遮挡，但不得破坏关键轮廓。
- 使用完整主体剪影、圆形小局部、窄纹理条和局部放大；不要把“撕裂照片块”当成一种常规裁切形式。
- 把纯色纸片、半调网点和抽象形状放在对象后方，充当视觉连接与色彩节奏，而不是用更多完整照片填空。

### 5. 根据素材选择背景与配色

不要设置固定默认底色，尤其不要无条件使用奶油黄。生成前先完成下面的配色决策：

1. 从全部照片中识别 2–4 个重复出现的主色，并记录 hero 的主要明度、饱和度和冷暖倾向；
2. 判断主题气质，例如海岛清爽、古建沉稳、都市冷峻、夜景霓虹、食物温暖、自然宁静、可爱活泼或随机视觉日记；
3. 为背景选择一个与 hero 有清晰明度或冷暖反差的低饱和纸张色，避免背景与最大主体同色融合；
4. 从素材已有颜色中选 2–3 个强调色，再按需要加入一个互补色；整张海报控制在 3–5 个主要色相；
5. 在提示词中写出本次实际选择的背景颜色名称与近似 hex，不要只写 `colorful background`、`light paper` 或沿用上次配色。

可参考但不要机械套用：

| 素材/主题倾向 | 可考虑的背景方向 |
|---|---|
| 海洋、蓝天、冷色旅行 | 沙白、浅珊瑚、雾粉、暖灰，避免再用大面积蓝色吞没主体 |
| 古建、历史、人文 | 低饱和青瓷绿、灰蓝、陶土粉、宣纸灰 |
| 城市、建筑、金属 | 冷灰、粉蓝、雾紫、暖白 |
| 绿植、山野、公园 | 淡紫、灰粉、浅天蓝、石灰白，避免绿色背景与植物粘连 |
| 食物、咖啡、暖色物件 | 鼠尾草绿、浅青、淡蓝灰、柔和米白 |
| 夜景、霓虹、深色素材 | 深海军蓝、炭灰、墨紫，搭配少量高亮色 |
| 可爱、玩具、糖果色 | 薄荷绿、浅粉、淡紫、粉蓝，选择与 hero 反差最大的一种 |

同一批素材再次生成时，若用户没有要求复刻，主动避开上一版背景色，探索另一种仍与素材协调的背景方向。

视觉语言保持：干净摄影剪影、细窄白色或浅色贴纸描边、轻微错位阴影、纯色纸片、少量半调网点和哑光纸纹理。摄影对象保持真实质感，装饰层保持平面图形感。避免儿童贴纸、廉价模板和装饰爆炸。不添加标题、日期、标签、数字、伪文字或水印；裁掉源照片文字，或将其缩小为不可读色块，除非用户明确要求保留。

用户指定其他风格时，仍须保留“独立对象抠图、单一环境锚点、撕纸只用于图形衬底、不做照片墙”四条核心规则。

### 6. 处理输入图数量限制

使用内置 `image_gen`。一次最多接收 5 个本地路径：

- 5 张以内的用户素材可直接传入；超过 5 张时，调用 `scripts/make_contact_sheet.py` 生成带编号素材板；
- 最多使用 5 张素材板。先用 `view_image` 检查素材板，再生成海报；
- 在提示词中逐一说明每个编号面板要提取的对象类型，并强调素材板本身绝不能出现在结果中；
- 临时素材板放在工作区 `tmp/imagegen/`，成品才复制到用户指定目录。

### 7. 组装提示词

使用以下结构，并保留其中的硬约束：

```text
Use case: compositing
Asset type: portrait travel-art poster
Source plan: panel/image number -> OBJECT_CUTOUT, SEMANTIC_CLUSTER, ENVIRONMENT_ANCHOR or MICRO_TEXTURE
Primary request: one finished colorful sticker-magazine collage; foreground is composed of background-removed semantic objects, not photo patches
Scene/backdrop: <theme-derived low-saturation paper color with approximate hex and reason for contrast>; at most one environment anchor covering no more than about 30% of the canvas
Subject: one cutout hero, 2–4 cutout secondary objects, supporting object stickers
Style/medium: contemporary Japanese pop-art travel zine; refined colorful sticker collage; clean photographic contour extraction; narrow light sticker outlines; bold flat paper shapes; playful oversized crops; subtle halftone dots and washi-paper texture; premium art direction rather than a children's scrapbook
Composition/framing: portrait 4:5, scale contrast, diagonal flow, clear margins and overlaps
Color palette: <3–5 colors derived from the photos; name the background and accent colors explicitly>
Text (verbatim): none
Hard constraints: at least 80% of photographic elements by count are isolated semantic cutouts; only one large environmental scene; torn paper is allowed only for non-photographic color shapes; no intact scene inside a torn edge; do not default to yellow; choose the background from this photo set's theme and hero contrast
Avoid: full-photo patches, torn-edge photographs, multiple scenic panels, scrapbook photo wall, equal-size thumbnails, pseudo-text, unrelated objects
```

明确写出每张照片要抠出的对象，尤其要把风景照片改写为“建筑/树/船/动物/车辆等独立对象”。同时写明本次背景色为何适合主题、如何与 hero 形成反差。不要只写“参考这些照片”，也不要泛写“撕纸拼贴”。

### 8. 检查并迭代

生成后逐项检查：

- 前景对象是否沿语义轮廓抠出，原背景是否已移除；
- 独立对象或语义对象组是否占摄影元素数量的至少约 80%；
- 是否只有 1 个大型环境锚点，且面积约不超过 30%；
- 是否出现第二个大型场景、撕边完整照片、照片墙或整块整块的场景拼接；
- hero 是否清晰，元素是否丰富但仍有留白；
- 背景色是否由本次主题和素材推导，是否与 hero 保持足够反差，而不是惯性使用黄色；
- 是否出现虚构对象、身份漂移、伪文字、标签或水印；
- 纯色衬底、描边、阴影和半调纹理是否统一。

若主体独立性不达标，使用下面的单一修正指令重新生成：

```text
Keep the current subject selection, color palette and hierarchy. Replace every intact or torn-edge photo patch except the single designated ENVIRONMENT_ANCHOR with clean background-removed semantic object cutouts. Follow each object's real contour. Put only flat-color or halftone paper shapes behind the objects. Do not retain any full scene, rectangular photo, torn photo border or scrapbook photo panel.
```

不要在同一轮同时更换主题、对象、构图和配色。

## 交付

将最终 PNG/JPEG 以版本化名称保存到工作区。说明识别出的主题、主要抠图对象、唯一环境锚点、风格方向和绝对文件路径。用户要求多种方向时，为每种方向单独调用一次 `image_gen`。
