> Historical D0 survey. Its initial identity-recognition recommendation was superseded by the requested fixed-region Face / Non-face pilot; see [current audit](README.md). Access results describe the D0 checks, not a new connectivity test.

> Public audit edition. Local filenames mentioned below are evidence references, not files included in this publication. See [audit index](README.md).

# D0 数据集调查 — 2026-10-19

结论：首选 **UWA HSFD v1.1 的小规模闭集、跨会话身份识别**，状态为 **Conditional**。数据真实可取得且有身份/会话标签，但独立样本少、辐射标定未知、顺序波段运动及许可冲突仍需处理。没有候选可以据此宣称已经适合大规模 Deep Unrolling 分类训练。

本目录是被 Git 忽略的本地研究工作区。原始归档保存在 `downloads/`；人脸不上传、不再分发。数据文件与源码、实验机完全分离。以下区分“官方描述”与“本次文件验证”，unknown 不代表不存在。

## 候选对照

| Dataset | 获取与许可 | 样本、标签、会话 | 波段、尺寸、数值定义 | 适配性与判定 |
|---|---|---|---|---|
| UWA HSFD v1.1 | 作者公开 Drive 原始归档已下载；IEEE 页面另有订阅入口。README 仅允许科研/学术、禁止商用和再分发，要求引用；目录 CC BY 4.0 与之冲突，暂采用更严格限制 | **实际**145 cubes/78 ID；S1=78、S2=48、S3=17、S4=2；目录为身份标签，145 个眼点文件对应有效 | **实际**1024×1024×33，uint8；作者声明400–720 nm/10 nm；数值按 DN/已处理强度处理，反射率/辐亮度标定 unknown | 名义21通道可选；17 ID可做S1/S2/S3三集合。**Conditional**：小规模身份识别；不能以patch/增强虚增独立样本 |
| PolyU HSFD | NIST目录可读；其官方数据链接404，现研究中心首页无可用HSFD入口；许可、现行申请条件 unknown；未下载 | NIST描述300 cubes/25人、多会话，每会话正/左/右3视角；实际逐身份会话数 unknown | 描述33 bands/400–720/10 nm；实际shape/dtype/辐射量 unknown | 描述上覆盖21点，但未验证文件、身份和授权。**Unavailable**（本轮无法核验获取），不等于断言永久下线 |
| Pavia University | EHU页面与数据文件请求403；未下载；数据使用许可 unknown，不能把网站/代码许可当作数据许可 | 官方目录9类、42,776标注像素，一个航空场景；像素不是42,776个独立物体 | 官方目录103 bands、1.3m像元；目录写610×610含无效区，常见处理文件610×340本轮未验证；实际中心/单位/dtype unknown | **Unavailable** 本轮获取受阻；方法上 **Conditional** 城市地物分类。没有原始中心坐标不能将103通道线性摊成450–650nm |
| CAVE Multispectral | 官方逐场景直接下载成功；页面明确向科研社区开放，未找到独立完整数据许可证，商业/再分发授权 unknown；引用Yasuma等 | 官方32场景/5展示分组；实际只下载balloons 1场景；没有经过验证的像素或物体分类标签，展示分组/文件名不作标签 | **实际**512×512×31 uint16；官方01=400、02=410…31=700 nm；由照明与相机响应校正得到的近似反射率，不是精确真值 | **Unsuitable** 分类主数据；**Conditional** 辅助物理输入。21名义通道直接对应；本轮未下载其余31场景 |
| ARAD_1K 31-channel | 官方GitHub指向CodaLab721，需注册；Windows原生证书连接200，未登录/未下载。公开规则限制于挑战范围内开放研究教育，随包另有条款；本项目用途需要核实 | 作者950公开HS图+50隐藏HS测试；论文900train/50val/50test；无身份/材料类别标签；跨场景独立性、近重复 unknown | 论文482×512×31，400–700/10 nm，是204原始波段经辐射校准与重采样结果；不能称31独立窄带原始采样 | **Unsuitable** 分类主数据；**Conditional** 辅助先验，当前访问/许可未完成。不能混用16通道400–1000版本 |

## 使用许可与来源证据

- UWA：[机构记录](https://research-repository.uwa.edu.au/en/datasets/uwa-hyperspectral-face-database/)、[作者下载页](https://sites.google.com/site/zohaibnet/Home/databases)、[IEEE DataPort](https://ieee-dataport.org/documents/uwa-hyperspectral-face-database)、DOI [10.21227/8714-kx37](https://doi.org/10.21227/8714-kx37)。本地 `source_evidence/UWA_archive_Readme.txt` 是归档原文；`Readme-HSFD.txt` 是DataPort公开说明，两者引用列表略不同，科研与不再分发限制一致。**不要据目录CC BY标记重新发布人脸或开放衍生脸图**；正式外部发布/商用前要求作者澄清。当前仅本地科研检查。
- UWA归档要求引用 Khan, Shafait & Mian, *Joint Group Sparse PCA for Compressed Hyperspectral Imaging*, TIP 2015, [DOI](https://doi.org/10.1109/TIP.2015.2472280)。DataPort说明另要求引用Uzair等TIP2015与BMVC2013人脸论文。引用条目原文均保留在本地README。
- PolyU：[NIST目录](https://tsapps.nist.gov/BDbC/Search/Details/330)、[旧官方入口](https://www4.comp.polyu.edu.hk/~biometrics/hsi/hyper_face.htm)、[当前中心](https://www4.comp.polyu.edu.hk/~biometrics/)。NIST的Active状态与本次404不同，不能据Active推断能下载。下一步需向维护者确认新地址与科研授权，本轮未发送申请。
- Pavia：[EHU原始分发目录](https://www.ehu.eus/ccwintco/index.php?title=Hyperspectral_Remote_Sensing_Scenes)、[数据文件](https://www.ehu.eus/ccwintco/uploads/e/ee/PaviaU.mat)。页面由搜索索引可读取，实时站点403；未使用未经授权镜像。类别像素数（目录值，非文件验证）：Asphalt6631、Meadows18649、Gravel2099、Trees3064、Painted metal sheets1345、Bare Soil5029、Bitumen1330、Self-blocking Bricks3682、Shadows947。类别严重不平衡；Shadows也不是材料种类。
- CAVE：[官方说明](https://cave.cs.columbia.edu/repository/Multispectral)、[Stuff下载页](https://cave.cs.columbia.edu/repository/Multispectral/Stuff)、[balloons原始包](https://cave.cs.columbia.edu/old/databases/multispectral/zip/balloons_ms.zip)。新站需JavaScript，已读取实际渲染页面；旧目录PHP错误不等于文件不可下载。参考 Yasuma等 *Generalized Assorted Pixel Camera*, CUCS-061-08, 2008，[官方论文](https://cave.cs.columbia.edu/Statics/publications/pdfs/Yasuma_TR08.pdf)。未把论文版权页误作数据许可证。
- ARAD：[作者README](https://github.com/boazarad/ARAD_1K)、[CodaLab721](https://codalab.lisn.upsaclay.fr/competitions/721)、[作者数据论文](https://openaccess.thecvf.com/content/CVPR2022W/NTIRE/html/Arad_NTIRE_2022_Spectral_Recovery_Challenge_and_Data_Set_CVPRW_2022_paper.html)。公开规则保存于 `source_evidence/arad_public_terms.txt`。需要账号和用途许可核查；未创建账号、接受协议或绕过登录。

## 波长与公平评测边界

UWA/CAVE 的文件序号06…26对应作者定义的450…650nm，保留所有原始波段，只记录选择映射，不做重采样。PNG本身没有可独立验证的光谱校准向量：这里验证的是文件编号与作者名义波段定义一致，而非测量中心/FWHM实证。采样间隔不等于光谱分辨率。ARAD31通道本身已经重采样；PolyU只是目录描述；Pavia的保留波段中心、有效通道掩码未取得，不允许猜测、外推或用RGB补通道。

UWA顺序LCTF成像存在运动风险；本次只验证眼点文件和完整立方体，**没有验收逐波段空间配准**。不同波段曝光与未知辐射处理也限制物理解释。后续模拟之前需要独立的配准/量化质量审核，不能把8bit强度直接声明为绝对反射率。

Pavia如以后取得合法数据与波长坐标，应使用互不重叠的空间块划分，按未来PSF/patch有效支持设置隔离带，训练、验证、测试都不得共享原始邻域；先查各类空间块覆盖，缺类时报告而非随机像素补齐。本轮没有文件，不生成虚假的像素ID划分。它是遥感城市地物分割，不代表实验室独立物体识别泛化。

本轮不扩展更多数据集：已经取得优先人脸候选和辅助场景，额外搜集无法消除当前样本规模与许可限制。
