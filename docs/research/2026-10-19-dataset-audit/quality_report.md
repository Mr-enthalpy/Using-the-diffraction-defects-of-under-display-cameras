> Public audit edition. Local filenames mentioned below are evidence references, not files included in this publication. See [audit index](README.md).

# D1-Data 标准化生产验收

2026-10-19。本轮实际生产了同域Face与Non-face样本。**可用于受限的“脸ROI vs 衣物/背景ROI”工程与探索性基线；尚不是通用人脸判别或光谱增益的科学基准。** 未修改minimal_operator.py、optic_system生产代码、实验机或Meta pin。

## 数量与划分

原始UWA v1.1：78身份、145次采集。先冻结46/16/16身份分组，对应85/30/30次采集；所有会话、ROI和增强继承身份所在集合，未按质量结果重新分配。

| 产物 | Train | Val | Test | 总数 |
|---|---:|---:|---:|---:|
| 接受的原始Face ROI | 41 | 11 | 9 | 61 |
| 接受的原始Non-face ROI | 39 | 10 | 9 | 58 |
| Face派生增强 | 41 | 0 | 0 | 41 |
| Non-face派生增强 | 39 | 0 | 0 | 39 |

**119份接受的原始ROI只来自61次原始采集，不能算119次独立测量。** 其中58次有通过筛查的成对正负ROI；这些成对数据用于oracle，按train/val/test分别39/10/9次采集。共80份派生增强，不新增独立测量。

全部manifest含286条：199条接受记录（119原始ROI+80增强）、80条待质量审核、1条待语义审核、6条裁剪越界失败。145原始Face提案中139份成功裁剪；61负候选来自61份接受Face的同次采集，其中58份通过筛查、3份因相位诊断低置信度待审核。所有失败记录保留，无静默删除。

## 真实标签审核

正类依据原始subject/session和眼点标注，固定眼距几何提案后，由Agent查看全部139份450/550/650nm三联图，判断是否包含完整脸部。未做身份、年龄等推断。[local sample ID withheld]在波段间显著转头，留待语义/运动审核；[local sample ID withheld]、[local sample ID withheld]的明显表情/眼部变化额外标记。审核者是Agent，不是独立现场人工标注员；详见 `review_decisions.json`。

负类不是猜文件名或借用CAVE。实际查看145份原图左下固定(0,768,256,256)候选的550nm内容，再对实际生产的61份查看450/550/650nm三联图：区域为衣物/背景，有些含非面部皮肤，没有可见人脸或面部轮廓。负类标签是本轮视觉审核产生，**不是作者发布的官方Non-face标注**。全部原始21波段来自同一UWA采集。

负类限制：共同幕布、固定左下位置、暗角、光照分布、衣物重复会产生捷径。脸ROI根据眼距裁剪后缩放，负ROI原尺寸256，不同空间尺度也有混杂。受试者/原始采集隔离已执行，背景场景隔离无法证明；不能把当前分数推广到手、动物、打印脸、显示器脸、陌生物体等。未创建跨传感器混合负类，也未生成RGB-to-HSI数据。

## 固定变换与格式

脸框：眼点中点向下0.5倍眼距，边长ceil(4×眼距)的方框；使用相同的原图整数ROI裁剪全部21band，OpenCV INTER_AREA确定性缩放到256×256。固定550nm为定位参考；未进行逐band配准、独立位移或伪造波段。眼点数值均有效，无需检测器回退；6个完整脸框越界并不被自动补边/移动，具体坐标在 `crop_rejections.json`。

每NPZ：`cube[21,256,256] float32`、`wavelengths_nm`、`mean_spectrum[21]`、`relative_spectrum[21]`、`pseudo_rgb[256,256,3]`及JSON metadata。原始8bit来源经过确定性面积插值后以float32保存，**不是新增传感器精度**。波长450:10:650，对应原始F_06…F_26。relative_spectrum为显式除以21点总和，原始mean另存。伪RGB仅650/550/450三个band以DN/255组合，不是标定RGB响应。

训练增强只使用OpenCV已有预处理及NumPy成熟数组操作：共同水平翻转和0.95–1.05的统一亮度倍率；随机seed由固定namespace与原始acquisition ID的SHA派生，记录parent/seed/参数。全部band使用同一参数，不截断float32值，不做ColorJitter或谱形变化。光谱与伪RGB从增强后cube重新计算。保留脸完整性优先，因此不启用平移、尺度、裁剪或旋转增强；验证和测试不做随机增强。Oracle未使用任何增强。

## 质量筛查与异常

全部成功文件验证shape、有限值、波长、目标重算、伪RGB一致性、SHA、group继承。源PNG和原始ZIP保持不变。Face候选有68次源ROI触及255，全部转待审；这只是保守筛查，不将255一概称为光学饱和。没有补值、删除波段或静默修正。

相位相关仅作成熟工具诊断：脸ROI对高斯平滑后的梯度幅值与550nm比较，负ROI对强度比较；response>=0.2且位移>4个输出像素触发待审，response<0.2也待审。阈值是工程审核触发器，不是经验证的配准精度。共18个Face候选触发疑似运动，Face低置信5个、负候选低置信3个；标记可重叠。不同光谱结构会导致假警报，局部眨眼/非刚性运动也可能漏检，未对数据施加相位位移校正。

“accepted”只表示当前标签/格式/粗筛条件通过，不保证逐像素光谱配准或辐射校准已成立。原始8bit量化、未知逐band曝光、未知精确滤波响应/黑电平仍存在。全库原始cube内容哈希无完全重复的D0检查结果已复用，当前文件/父来源再次校验；未宣称近重复全面排除。

6个越界提案：[local sample ID withheld]、[local sample ID withheld]、[local sample ID withheld]、[local sample ID withheld]、[local sample ID withheld]、[local sample ID withheld]。接近边界或可疑眼点语义应单独复核，不通过自动调框掩盖。

## 运行与复现

已有环境：`optic_system/.venv/Scripts/python.exe`，NumPy、OpenCV、Pillow、PyYAML、SciPy，无新环境或依赖安装。生产代码在本目录，输出只写这里。依次运行：

```powershell
.\optic_system\.venv\Scripts\python.exe -X utf8 outputs/d1_data_20261019/dataset_build.py
# 查看dataset_preview并形成review_decisions.json后：
.\optic_system\.venv\Scripts\python.exe -X utf8 outputs/d1_data_20261019/dataset_build.py --finalize
.\optic_system\.venv\Scripts\python.exe -X utf8 outputs/d1_data_20261019/dataset_build.py --negatives
# 检查负类三联图后：
.\optic_system\.venv\Scripts\python.exe -X utf8 outputs/d1_data_20261019/dataset_build.py --augment-negatives
.\optic_system\.venv\Scripts\python.exe -X utf8 outputs/d1_data_20261019/validate_build.py
.\optic_system\.venv\Scripts\python.exe -X utf8 outputs/d1_data_20261019/oracle_check.py
```

目录已存在时生产脚本拒绝覆盖；复建请复制配置/脚本/审核记录至新的本地忽略目录并重新指定相对输入路径，不删除原产物。脚本是本数据集的固定流程，不是通用数据平台。`dataset_manifest.csv`是消费入口：只用accepted状态且明确选择augmentation策略，不能遍历built目录把候选中间文件重复计入。

`validate_build.py`实际通过所有列出的数值/哈希/划分/增强重放检查，详见 `validation_summary.json`。没有运行硬件测试、没有训练N1。`final_production_receipt.json`固定配置、脚本、manifest和审核记录的版本；首次生产阶段的版本另存 `build_versions.json`。

## 许可和下一步

沿用D0原始README的本地科研/学术范围、禁止商用和再分发；目录宽泛许可与README冲突没有被忽略。原始及派生人脸、预览、模型和manifest均在Git忽略目录，没有公开上传。本轮只交付本地成果。

结论：**标准化工程链路和受限正负样本已交付，可以审查后用于限定场景的后续实验输入；当前不足以验收通用Face/Non-face或“超越RGB”。** 不自动进入PSF仿真或Deep Unrolling。先审查固定背景、ROI位置/尺度、光谱标定和严格RGB对照这些限制。
