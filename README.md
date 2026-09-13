<p align="center">
  <img src="assets/hero.svg" width="100%" alt="标书工作台 — 让每一次投标复核，都有据可查。" />
</p>

<p align="center">
  面向 Windows 的本地标书检查与材料整理工具<br />
  从企业与人员资料，到投标文件核对，再到人工终审与归档。
</p>

<p align="center">
  <a href="https://github.com/yaoyouzhong/Bidding-releases/releases/download/v0.4.0/Biaoshu_0.4.0_x64-setup.exe"><strong>下载 Windows 安装包 ↗</strong></a>
  &nbsp; · &nbsp;
  <a href="https://github.com/yaoyouzhong/Bidding-releases/releases/latest">版本与下载</a>
  &nbsp; · &nbsp;
  <a href="#开始使用">开始使用</a>
  &nbsp; · &nbsp;
  <a href="#自动更新">自动更新</a>
</p>

<p align="center"><sub>Windows 10 / 11 · x64 &nbsp;&nbsp; | &nbsp;&nbsp; 本地资料管理 &nbsp;&nbsp; | &nbsp;&nbsp; AI 增强按需开启</sub></p>

---

> **使用用途：仅供学习与交流，不用于任何商业用途。**
> 本项目免费提供，用于学习和交流文档处理、OCR 与信息核对技术；请勿用于商业投标、收费服务或其他商业活动。
> 第三方组件仍按各自许可证提供；本声明不替代其许可，也不表示已取得第三方额外授权。

## 把复核工作，组织成一条清晰的流程

标书工作台将材料整理、文件检查、问题处理与归档衔接起来。识别结果保留原件依据，机器发现交由人工核对，让材料、问题与处理记录能够对应起来。

| 工作环节 | 可以完成的工作 |
| :--- | :--- |
| **企业与人员资料** | 整理证照、资质和人员证件，使用本地 OCR 辅助识别与复核。 |
| **官网查询与留存** | 通过专用 Chrome 会话查询企业信用、核验学历，按查询流程保存证据。 |
| **投标文件检查** | 检查格式与完整性，核对招标要求的响应情况，并保留问题来源。 |
| **多公司文件查重** | 比较不同公司的投标文件，查看命中内容与原件证据，逐项人工核查。 |
| **问题处理与交付** | 处理检查问题，完成人工终审，将文件与复核记录归档留存。 |

> **判断由人作出，依据保留下来。** 机器检查提供复核线索，不自动认定得分或违规；归档也不代表已向招标方递交。

## 开始使用

**1. 安装工作台**  
普通用户选择 **EXE 安装包**，保留默认安装位置即可使用应用内更新。无需另装 Python、Node 或 Rust。

**2. 建立投标人和项目**  
按当前项目整理企业、人员资料，导入招标文件与投标文件。

**3. 检查、复核、归档**  
结合原件核对检查结果，处理问题，再进行人工终审与交付归档。

| 安装方式 | 适合的使用方式 | 下载 |
| :--- | :--- | :--- |
| **EXE · 推荐** | 当前用户安装，支持应用内更新 | [下载 0.4.0](https://github.com/yaoyouzhong/Bidding-releases/releases/download/v0.4.0/Biaoshu_0.4.0_x64-setup.exe) |
| **MSI** | 机器级安装或集中部署，使用安装包升级 | [下载 0.4.0](https://github.com/yaoyouzhong/Bidding-releases/releases/download/v0.4.0/Biaoshu_0.4.0_x64.msi) |

<details>
<summary><strong>安装环境与下载校验</strong></summary>

- 支持 Windows 10 / 11 x64。
- 界面使用 Microsoft Edge WebView2，首次安装建议保持联网。
- 企业信用与学历官网查询需要安装 Google Chrome；需要人工验证时，按官网提示操作。
- 安装包尚未取得 Windows Authenticode 签名；可通过同版 [SHA256SUMS.txt](https://github.com/yaoyouzhong/Bidding-releases/releases/download/v0.4.0/SHA256SUMS.txt) 核对文件完整性。
- EXE 与 MSI 选择一种即可。

</details>

## OCR 模型

在应用设置点击“下载模型”，或[下载完整离线模型包](https://github.com/yaoyouzhong/Bidding-releases/releases/download/models-v1/models-v1-offline.zip)后点击“导入模型”，无需解压。已有模型可跨程序升级复用。

## 自动更新

**从 0.3.0 开始，更新能力已包含在程序中。**

启动后自动检查新版本。发现更新时，应用设置中显示提醒；查看说明、保存工作并确认后，点击 **「一键升级」**，程序会下载并验证签名，安装完成后重启。

更新前保留旧版备份，新版启动失败时尝试恢复旧版。后台任务运行期间不能安装更新；机器级 MSI 安装，以及涉及数据库结构变化的版本，使用另行验证的完整安装包升级。

## 本次版本

**0.4.0** 将 OCR 模型与程序分开分发，减少安装和升级体积；新增模型下载与导入、操作反馈和版本显示，并修复验证码过期及重复提交问题。

[阅读完整版本说明 →](RELEASE_NOTES.md)

<details>
<summary><strong>已验证范围与当前边界</strong></summary>

- EXE 与 MSI 分别通过全新 Windows Sandbox 的 **22 项安装生命周期检查、15 项合成业务检查**。
- 应用内更新通过正常升级、无效程序恢复、启动失败恢复及中断恢复 **4 个场景**，逐项核对原项目数据库未变化。
- 本轮不包含无 WebView2 的离线安装、同版本覆盖安装、真实个人学信网查询及跨机器 GPU 性能验收。

</details>

## 数据与可选 AI

材料默认保存在本机。AI 增强默认关闭，配置模型并明确开启相应用途后，才发送相关内容。官网查询按用户发起的操作访问对应网站；请按业务需要备份重要资料。

反馈问题时，请提供脱敏后的操作步骤和错误提示，**不要上传真实投标材料、身份证件、项目数据库或密钥**。

## 关于本仓库

这里是标书工作台的**公开分发仓库**，提供安装包、签名更新包、校验值与使用说明。业务源码及开发历史保留私有。

[第三方组件说明](THIRD_PARTY_NOTICES.md) · [GEOS 分发与兼容库说明](GEOS_DISTRIBUTION.md) · [全部版本](https://github.com/yaoyouzhong/Bidding-releases/releases)

<details>
<summary>第三方许可证与源码资料</summary>

Release 中的 `licenses.zip` 提供第三方许可证原文，`sources.zip` 仅包含第三方库源码及构建参考，不是标书工作台业务源码。相关材料也位于安装目录的 `third-party.zip`，随程序更新或恢复。

第三方组件按各自许可证提供，相应权利不受本程序其他说明限制。GEOS 的使用与修改权利见对应说明，普通用户无需替换该库。

</details>

---

<p align="center"><sub>标书工作台 · 整理有序，复核有据。</sub></p>
