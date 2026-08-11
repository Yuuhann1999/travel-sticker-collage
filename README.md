# 彩色贴纸旅行拼贴

一个面向 Codex、Claude Code 及其他 AI Agent 的多照片拼贴海报 Skill。

它会从至少两张照片中自动判断共同主题，沿语义轮廓提取人物、动物、食物、商品、地标和细节，把它们重新组织成一张彩色贴纸杂志风海报。主题明确时建立旅行或活动叙事；照片较随机时，则从颜色、形状、材质和动作方向中寻找视觉共性。

这个 Skill 的重点不是把照片做成撕纸照片墙，而是让大部分摄影元素成为背景被移除的独立对象。每张海报只允许一个主要环境画面，其余风景照片优先提取建筑、树、船、车辆、动物等具体对象。

## 安装

使用 `skills` CLI：

```bash
npx -y skills add Yuuhann1999/travel-sticker-collage \
  --global --skill travel-sticker-collage
```

也可以手动安装到通用 Agent Skills 目录：

```bash
cp -R ./travel-sticker-collage ~/.agents/skills/
```

安装到 Codex：

```bash
cp -R ./travel-sticker-collage ~/.codex/skills/
```

## 使用

安装后，在对话中上传至少两张照片并调用：

```text
使用 $travel-sticker-collage，把我上传的照片做成一张 4:5 竖版彩色贴纸杂志海报。
自动判断共同主题，不加文字。主体按真实轮廓独立抠出，只保留一张风景作为环境锚点。
```

如果只有两张照片，Skill 会尽量从每张照片中分别提取主主体、次物件、纹理和局部细节；照片较多时，则保证每张照片至少贡献一个可辨识元素，同时维持主次关系。

## 核心规则

- 至少约 80% 的摄影元素按数量呈现为独立对象或语义对象组。
- 人物、动物、食物、商品和地标默认移除原始背景，沿真实轮廓裁切。
- 每张海报最多保留一个大型环境画面，占画布约不超过 30%。
- 撕纸、网点和胶带只用于纯色色块与抽象纹理，不包裹完整照片。
- 禁止完整照片块、多个大型风景面板、等尺寸缩略图和照片墙。
- 默认使用一个 hero、2–4 个 secondary，以及若干小型 supporting elements。
- 默认画幅为 4:5 竖版，不添加标题、标签、日期、伪文字或水印。

## 照片数量策略

| 照片数量 | 处理方式 |
| --- | --- |
| 2 张 | 每张提取 3–5 个不同元素，让两张照片共同支撑画面 |
| 3–5 张 | 每张至少一个独立主体，再补充纹理或局部细节 |
| 6–12 张 | 设置一个主视觉，每张贡献 1–2 个主体或小型锚点 |
| 13 张以上 | 合并相近对象形成节奏，风景转为地标抠图或小型环境窗口 |

参考图片数量超过图像工具的单次限制时，Skill 会调用随附的 `make_contact_sheet.py`，把照片整理成带编号的临时素材板，再逐一说明每张照片需要提取的对象。

## 示例效果

下面的海报由九张旅行照片生成。海豚承担主视觉，鱼群、食物、人物装置和饮料以独立抠图出现，海滩是唯一的大环境画面。

<p align="center">
  <img src="examples/example-poster.png" alt="彩色贴纸旅行拼贴海报示例" width="560">
</p>

## 推荐工作流程

```text
上传照片
    ↓
判断共同主题或视觉共性
    ↓
把每张照片分类为独立对象、语义对象组、环境锚点或微型纹理
    ↓
生成彩色贴纸杂志海报
    ↓
检查主体抠图、环境数量、文字与视觉层级
```

## 项目结构

```text
travel-sticker-collage/
├── travel-sticker-collage/
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── assets/
│   │   └── independent-cutout-reference.png
│   └── scripts/
│       └── make_contact_sheet.py
├── examples/
│   └── example-poster.png
├── LICENSE
└── README.md
```

## 依赖与说明

- 本仓库提供 Skill 指令、Agent 元数据、素材板脚本、风格参考和示例图，不包含图像模型、图片生成 API 或 API Key。
- 实际生成需要宿主 Agent 具备图片查看和图片生成能力。
- `scripts/make_contact_sheet.py` 需要 Python 3 与 Pillow。
- `assets/independent-cutout-reference.png` 是 Skill 的视觉参考组成部分，安装时不要单独复制 `SKILL.md`。
- 图像模型存在随机性。正式使用前应检查主体是否被完整抠出、是否出现多余环境照片、文字、标签或水印。

## 许可证

Skill 指令与脚本使用 [MIT License](LICENSE)。示例图和参考图可能包含第三方商标、角色或商品形象；相关权利归各自权利人，仓库许可证不会转移这些第三方权利。
