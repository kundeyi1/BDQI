import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']


# 读取数据并计算协方差矩阵
data = pd.read_csv('returns.csv', index_col=0)*100
train_data = data[(data.index >= '2022-01-01') & (data.index <= '2023-06-30')]
test_data = data[(data.index > '2023-06-30')]
cov = train_data.cov().values
n = cov.shape[0]

# 风险平价组合权重计算
# 1. 定义目标函数
def risk_parity_objective(w, cov):
    port_var = w @ cov @ w               # 组合方差
    mrc = cov @ w                        # 边际风险贡献 (MRC)
    rc = w * mrc                         # 风险贡献 (RC)
    target_rc = port_var / n             # 平价目标：每个资产贡献 port_var / n
    return np.sum((rc - target_rc) ** 2)

# 2. 设置约束和边界
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
bounds = [(0, 1) for _ in range(n)]      # 无卖空
x0 = np.ones(n) / n                      # 初始猜测：等权

# 3. 优化求解
result = minimize(
    risk_parity_objective,
    x0,
    args=(cov,),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

w_rp = result.x

# 4. 输出结果
rc = w_rp * (cov @ w_rp)
print("风险平价权重:", w_rp)
print("各资产风险贡献:", rc)
print("是否近似平价？最大相对误差:", np.max(np.abs(rc - rc.mean())) / rc.mean())


# 等权组合权重
w_eq = np.ones(len(w_rp)) / len(w_rp)

# 均值方差组合权重
def max_sharpe_ratio(weights, returns):
    portfolio_return = np.sum(returns.mean() * weights)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov(), weights)))
    sharpe_ratio = portfolio_return / portfolio_volatility
    return -sharpe_ratio  # 最大化夏普比率

constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = [(0, 1) for _ in range(len(w_rp))]
initial_guess = w_eq

opt_result = minimize(max_sharpe_ratio, initial_guess, args=(train_data,), method='SLSQP',
                      bounds=bounds, constraints=constraints)
w_mv = opt_result.x


# 基于测试集的对比分析

# 计算各组合的日度收益
portfolio_returns_rp = test_data.dot(w_rp)
portfolio_returns_eq = test_data.dot(w_eq)
portfolio_returns_mv = test_data.dot(w_mv)

# 计算年化波动率和夏普比率
def annualized_metrics(returns):
    daily_mean = returns.mean()
    daily_volatility = returns.std()
    annual_volatility = daily_volatility * np.sqrt(252)  # 假设每年交易日为252天
    sharpe_ratio = daily_mean / daily_volatility * np.sqrt(252)
    return annual_volatility, sharpe_ratio

vol_rp, sr_rp = annualized_metrics(portfolio_returns_rp)
vol_eq, sr_eq = annualized_metrics(portfolio_returns_eq)
vol_mv, sr_mv = annualized_metrics(portfolio_returns_mv)

print(f"风险平价组合年化波动率: {vol_rp:.4f}, 夏普比率: {sr_rp:.4f}")
print(f"等权组合年化波动率: {vol_eq:.4f}, 夏普比率: {sr_eq:.4f}")
print(f"均值方差组合年化波动率: {vol_mv:.4f}, 夏普比率: {sr_mv:.4f}")

# 绘制风险贡献分布图
def plot_risk_contributions(w, cov, title):
    rc = w * (cov @ w)
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(rc)), rc, color='skyblue')
    plt.title(title)
    plt.xlabel('资产')
    plt.ylabel('风险贡献')
    plt.xticks(range(len(rc)), test_data.columns, rotation=45)
    plt.tight_layout()
    plt.savefig(f'{title}.png')

# 计算测试期协方差矩阵
cov_test = test_data.cov().values

plot_risk_contributions(w_rp, cov_test, '风险平价组合风险贡献')
plot_risk_contributions(w_eq, cov_test, '等权组合风险贡献')
plot_risk_contributions(w_mv, cov_test, '均值方差组合风险贡献')

# 风险平价权重: [0.06072605 0.09654299 0.11850184 0.0755955  0.14076409 0.14492804
#  0.06562179 0.07465913 0.12546052 0.09720004]
# 各资产风险贡献: [0.08496693 0.08447169 0.08501097 0.08481865 0.08490196 0.08491526
#  0.08482652 0.08480408 0.0849832  0.0849753 ]
# 是否近似平价？最大相对误差: 0.0046633688011455685
# 风险平价组合年化波动率: 15.5359, 夏普比率: 1.7175
# 等权组合年化波动率: 16.3897, 夏普比率: 1.5477
# 均值方差组合年化波动率: 19.1530, 夏普比率: 1.6275