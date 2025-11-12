import pandas as pd
from matplotlib.dates import AutoDateLocator
import matplotlib.pyplot as plt
import statsmodels.api as sm


# 数据导入
brk = pd.read_csv('alpha_brk.csv',
                  skiprows=0,
                  header=0,
                  index_col='date'
                  )

factor = pd.read_csv('factor.csv',
                     skiprows=0,
                     header=0,
                     index_col='ym'
                     )

# 处理数据
brk.index = pd.to_datetime(brk.index, format='%m/%Y')
factor.index = pd.to_datetime(factor.index, format='%Y%m')
brk = brk / 100 # 转化为统一单位

# merge
merged_df = pd.merge(brk.iloc[:,0], factor, left_index=True, right_index=True, how='inner')
merged_df.corr()

# 定义多因子组合
models = {
    'CAPM': ['Mkt_RF'],
    'FF3': ['Mkt_RF', 'SMB', 'HML'],
    'FF5': ['Mkt_RF', 'SMB', 'HML', 'RMW', 'CMA'],
    'FF5_MOM': ['Mkt_RF', 'SMB', 'HML', 'RMW', 'CMA', 'MOM']
}

# 因子组合检验函数
def factor_test(merged_df, factors):
    y = merged_df.iloc[:,0]
    x = sm.add_constant(merged_df[factors])
    print(x, y)
    model = sm.OLS(y, x).fit()
    print(f"Model: {model_name}, Factors: {factors}")
    print(model.summary())

    #计算累计alpha
    alpha = y - model.fittedvalues
    alpha_cum = alpha.cumsum()

    #绘制图形
    plt.gca().xaxis.set_major_locator(AutoDateLocator())
    plt.plot(alpha_cum)
    plt.title('Cumulative Alpha for BRK using ' + ', '.join(factors))
    plt.savefig(f"{'_'.join(factors)} Cumulative Alpha for BRK.png")
    plt.close()

    return alpha_cum

# 回归模型
alpha = {}
for model_name, factors in models.items():
    alpha[model_name] = factor_test(merged_df, factors)

