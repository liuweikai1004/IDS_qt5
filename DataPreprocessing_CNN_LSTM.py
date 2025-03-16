import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from tqdm import tqdm
import psutil
from joblib import Parallel, delayed
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.model_selection import train_test_split


# 1. 数据加载与预处理
def load_data_csv(path):
    # 添加CSV格式特有参数
    data = pd.read_csv(path,
                       sep=',',  # 分隔符，根据实际数据调整
                       encoding='utf-8')  # 编码方式，中文数据可尝试 'gbk'

    # 分类特征设置（请根据实际数据字段确认）
    categorical_cols = ['proto', 'service', 'state']  # UNSW-NB15典型分类特征
    label_encoders = {}

    # 分类特征编码
    for col in categorical_cols:
        if col in data.columns:
            # 填充缺失值为 'unknown'，并转换为字符串
            data[col] = data[col].fillna('unknown').astype(str)
            # 初始化新的编码器
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            label_encoders[col] = le  # 保存编码器
        else:
            print(f"Warning: 分类特征列 {col} 不存在于数据集中，已跳过")

    # 数值型缺失值处理（排除分类特征）
    numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col not in categorical_cols]
    data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

    # 定义攻击类型到数值的映射
    attack_cat_mapping = {
        'Normal': 0,
        'Fuzzers': 1,
        'Analysis': 2,
        'Backdoors': 3,
        'Dos': 4,
        'Exploits': 5,
        'Generic': 6,
        'Reconnaissance': 7,
        'Shellcode': 8,
        'Worms': 9
    }

    # 如果 attack_cat 列存在
    if 'attack_cat' in data.columns:
        # 填充缺失值为 'unknown'（如果有）
        data['attack_cat'] = data['attack_cat'].fillna('unknown')
        # 将 attack_cat 列的值映射为数值
        data['attack_cat'] = data['attack_cat'].map(attack_cat_mapping).fillna(-1).astype(int)  # 未知类别标记为 -1
    else:
        print("Warning: 'attack_cat' 列不存在于数据集中")

    # 添加数据打印
    print("\n=== 数据加载报告 ===")
    print(f"数据集形状: {data.shape}")
    print("前3行样本:")
    print(data.head(3))
    print("\n特征类型分布:")
    print(data.dtypes.value_counts())
    print("\n标签分布:")
    print(data['label'].value_counts(normalize=True))
    print("缺失值统计:")
    print(data.isnull().sum().sort_values(ascending=False).head(5))
    print("=" * 40)
    return data

# 3. 数据预处理主函数
def preprocess_data(test_path, selected_features, timesteps):
    # 加载数据
    print("加载数据...")
    data = load_data_csv(test_path)


    # 筛选特征并处理
    X = data[selected_features]

    # 标准化和归一化处理
    print("标准化和归一化处理...")

    # 第一步：归一化处理
    minmax_scaler = MinMaxScaler()
    X_test_normalized = minmax_scaler.fit_transform(X)

    # 第二步：标准化处理
    standard_scaler = StandardScaler()
    X_test_processed = standard_scaler.fit_transform(X_test_normalized)

    # 转换为3D格式 (samples, timesteps, features)
    X_test_3d = create_sliding_windows(X_test_processed, timesteps)

    return X_test_3d
def create_sliding_windows(data, timesteps):
    X = []
    for i in range(len(data) - timesteps + 1):
        X.append(data[i:i+timesteps])
    return np.array(X)
