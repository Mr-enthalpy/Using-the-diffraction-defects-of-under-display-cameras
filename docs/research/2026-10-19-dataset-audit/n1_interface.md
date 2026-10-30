> Historical D1 interface checks: the unlabelled 290 candidate curves are distinct from the later D1-Data production. Current label acceptance is reported in [quality_report.md](quality_report.md). No N1 training has started.

> Public audit edition. Local filenames mentioned below are evidence references, not files included in this publication. See [audit index](README.md).

# N1 最小离线接口与数值验收

本轮仅在Git忽略研究目录实现 `minimal_operator.py`，不修改optic_system、实验机或Meta pin，不实现Deep Unrolling网络。独立使用既有Python环境的NumPy/SciPy；代码无SDK导入。

## 实测数据与核处理

输入为 `spectral21_20261018_reset01/roi_extent_review/roi1024_<nm>.npz` 全21份；读取每份PSF数组、sensor ROI、波长、相机读回/请求曝光，计算SHA，记录在 `psf_kernel_audit.json`。RawCapture文件盘点沿用D0位置，原始数据不改动。

固定1024窗口 `(866,554,1024,1024)`；512窗口为其中心子块 `(1122,810,512,512)`。从匹配曝光的pre/post dark mean均值扣暗，再扣1024边缘40像素残差均值；512共享该大窗口背景。本次数值signed能量比512/1024为0.929952–1.025299，超过1是背景敏感性而非能量增加。两者均没有被证明包住完整PSF，1024也可能截断远尾。

每band核在分析副本显式除以各自signed sum，用于**shape-only数值实验**；负噪声保留，负像素比例记录。它不是无噪声非负光学PSF。没有默默正截断以增加尾部能量；如何估计物理非负核仍是后续质量问题。

曝光201.821/403.643/1614.571µs不一致；相机gain为0dB。原始不同曝光DN总和不能作光谱灵敏度。即使除曝光，仍含氙灯光谱功率、滤光片、未知单色仪带宽、CFA/传感器和光路响应；缺少已知输入光谱功率，无法分离绝对throughput。当前operator强制显式传入21个非负weights；测试使用全1，**不是实验校准结果**。

## 前向与伴随

记空间光谱输入为`X[21,H,W]`：

`A(X) = sum_b w[b] * C(full_convolution(X[b], K[b]))`

零延拓，先full线性卷积，C裁剪从`(kernel_height//2,kernel_width//2)`开始的H×W窗口。偶数核也严格使用这个整数原点，不用隐式fftshift或各band独立对齐；共同原点对应sensor `(1378,1066)`，是约定而非每band峰值。

`A*(Y)[b] = w[b] * valid_convolution(C*(Y), reverse(K[b]))`

C*将Y放回同一full输出尺寸，其余补零。伴随输入`[H,W]`，输出`[21,H,W]`。有限、维度检查明确报错。当前是实数标量测量原型，没有擅自假设RGB传感器响应。

RAW8来自Bayer相机，整幅测得核混有CFA周期响应；任意单像素平移不必满足LTI。缺少场依赖PSF、CFA子格/相位处理和已知RGB谱响应，本operator只能作为数值shape近似，不能称为已校准的真实相机forward。空间离散尺度和放大率也尚未映射到UWA像素；本轮不将UWA直接卷积成训练数据。

## N1监督与一致性

`spectral_target(X[batch,21,H,W]) -> [batch,21]`为相同ROI均值，后续若选择相对谱则显式sum-one并检查有效性。输出独立导出，质量状态与不确定性另列，不与C1 embedding混同。

测量残差形式 `0.5*||A(Xhat)-Y||²` 对X的梯度是 `A*(A(Xhat)-Y)`。**不能直接把21维均值z送进A**：A需要空间分布。已构造同均值、不同位置的两个立方体，测量差异非零。未来unrolling需明确空间状态/空间基或其他已验证的空间模型，最后抽取21维目标；这只是接口约束，本轮不实现完整cube恢复网络，也不把恢复完整光谱立方体作为验收目标。

仅21维谱加固定空间模板的简化模型，必须先证明模板适用；当前未证明，不提前实现。C1为逻辑上的二分类头，C2/C3仅文档概念，无空模块。

## 实际数值测试

命令（Meta根目录）：

```powershell
.\optic_system\.venv\Scripts\python.exe -X utf8 outputs/d1_face_spectral_20261019/inspect_curves.py
.\optic_system\.venv\Scripts\python.exe -X utf8 outputs/d1_face_spectral_20261019/check_operator.py
.\optic_system\.venv\Scripts\python.exe -X utf8 outputs/d1_face_spectral_20261019/final_checks.py
```

结果见 `operator_checks.json`：512/1024实际21band核内积伴随相对误差分别8.12e-16、1.15e-15；非对称偶数小核对直接卷积最大差7.11e-15；loss方向导数相对误差5.46e-11；线性、无效shape/NaN拒绝通过。同一X用同一operator生成再检验的残差为0，这只是实现自洽，**不是实测模型拟合验收**。实际核测试使用8×9数值输入以控制内存，不代表完整场景性能。

## 下一轮决定

**暂不启动N1训练。** 先取得可信的Face/Non-face标签及场景隔离方案，并验收光谱曲线在匹配RGB对照下的判别价值；同时明确光谱幅值/照明标定、CFA与空间不变近似、PSF支持尾部、目标数据辐射解释和空间尺度。当前可继续做有限数据审核/接口研究，但不能把数值伴随通过当作训练物理条件齐备。
