# 基金的投资业绩的 alpha 来源分析作业

## 1. 数据说明
### 1.1 时间长度
题目给出了1990年6月至2013年12月的Berkshire Hathaway Inc (%Total Return)以及Excess Return (monthly) in percent（累计收益率和月超额收益），给出了2000年1月到2025年6月的各项因子取值，这里只能使用其中重合的时间，即2000-2013，进行累计Alpha分析。

### 1.2 数据质量
观察到alpha_brk.csv和factor.csv中的文件在相同因子、相同时间上的取值有所不同，这里采用factor.csv的数据作为回归的解释变量；并对alpha.csv中的Excess Return (monthly) in percent除以100以还原原始数据、统一量纲。

## 2. 累计Alpha曲线
### 2.1 CAPM
![alt text](<Mkt_RF Cumulative Alpha for BRK.png>)

### 2.2 Fama-French 三因子
![alt text](<Mkt_RF_SMB_HML Cumulative Alpha for BRK.png>)

### 2.3 Fama-French 五因子
![alt text](<Mkt_RF_SMB_HML_RMW_CMA Cumulative Alpha for BRK.png>)

### 2.4 Fama-French 五因子以及动量
![alt text](<Mkt_RF_SMB_HML_RMW_CMA_MOM Cumulative Alpha for BRK.png>)

## 3. 结果解释
### 3.1 整体差异小
四张曲线图整体差异很小：BRK 的收益主要由市场风险（Mkt_RF）驱动，其他风格暴露较小。
主要区别为：随着因子的增加，累计Alpha波动变得更小，意味着累计Alpha能被因子解释的部分增加。

### 3.2 基金业绩来源
| 模型       | 未显著提升解释性的原因                                                  |
|------------|----------------------------------------------------------------------|
| CAPM       | 仅用市场风险，无法解释全部收益                                       |
| FF3        | SMB/HML 对 BRK 影响小（不偏向小盘或高盈利）                        |
| FF5        | RMW/CMA 是盈利和投资风格，BRK 多投成熟企业，这类因子贡献低           |
| FF5+MOM    | 动量因子对 BRK 影响极弱（不追涨杀跌）                              |

此外，回归结果显示，仅采用Mkt_RF作为解释变量时， $\R^{2}$ 仅为0，001，考虑FF5因子+动量时，$\R^{2}$仍然只有0.015，BRK的超额收益还有大量未能被解释的部分。