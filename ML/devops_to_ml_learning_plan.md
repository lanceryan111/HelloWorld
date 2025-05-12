
# DevOps 向 AI/ML 工程师转型学习计划（12 周）

> 适用于具备 Python 和 Azure 基础的 DevOps 工程师  
> 作者建议：边学边做，构建 GitHub 项目 + 实战总结

---

## ✅ 阶段一：Python 数据分析基础（第 1-2 周）

### 学习内容：
- Python 数据结构、Numpy、Pandas
- 数据清洗与处理
- 可视化（matplotlib / seaborn）

### 推荐资料：
- [Python Data Science Handbook 中文版](https://github.com/itpluscode/data-science-handbook-chinese)
- [Seaborn 官网教程](https://seaborn.pydata.org/tutorial.html)
- [Kaggle Notebooks](https://www.kaggle.com/notebooks)

### 实战练习：
- Titanic 生存预测
- 泰坦尼克乘客数据分析可视化

---

## ✅ 阶段二：机器学习基础（第 3-4 周）

### 学习内容：
- 监督学习模型（回归、分类）
- 模型评估指标（准确率、F1、ROC）
- 模型保存与加载

### 推荐资料：
- [Scikit-learn 中文文档](https://sklearn.apachecn.org/)
- [Kaggle 房价预测竞赛](https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques)

### 实战练习：
- 房价预测
- 模型持久化 + 预测脚本

---

## ✅ 阶段三：Azure ML 入门（第 5-6 周）

### 学习内容：
- 创建 Azure ML Workspace
- 使用 Notebook 进行训练任务
- AML SDK 使用（数据集、训练、注册模型）

### 推荐资料：
- [Azure ML 入门指南](https://learn.microsoft.com/zh-cn/azure/machine-learning/quickstart-create-resources)
- [Azure ML GitHub 示例项目](https://github.com/Azure/MachineLearningNotebooks)

### 实战练习：
- 在 Azure 上训练分类模型并注册为模型资产

---

## ✅ 阶段四：模型部署 & API 服务（第 7-8 周）

### 学习内容：
- 使用 Azure Online Endpoint 部署模型
- 生成 API 接口，支持 RESTful 调用
- 使用 Postman/Python 客户端调用接口

### 推荐资料：
- [Azure Online Endpoint 部署文档](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-deploy-online-endpoints)

### 实战练习：
- 模型 API 部署
- 创建 Swagger 文档或 Python 客户端调用 demo

---

## ✅ 阶段五：MLOps 实践（第 9-10 周）

### 学习内容：
- 使用 MLflow 进行实验跟踪
- 使用 Azure ML Pipelines 管理训练 + 部署流程
- 使用 GitHub Actions 实现 CI/CD

### 推荐资料：
- [MLflow 官方文档](https://mlflow.org/docs/latest/index.html)
- [Azure MLOps 示例](https://github.com/microsoft/MLOps)

### 实战练习：
- 自动训练 + 注册 + 部署模型流水线
- 使用 YAML + Action 实现自动化

---

## ✅ 阶段六：深度学习与 NLP（第 11-12 周）

### 学习内容：
- PyTorch 基础（张量、模型训练、优化器）
- Transformer & Hugging Face
- 在 Azure 使用 GPU 实例训练

### 推荐资料：
- [PyTorch 教程](https://pytorch.org/tutorials/)
- [Hugging Face 中文课程](https://hf.shuniu.top/)
- [Azure GPU 使用教程](https://learn.microsoft.com/en-us/azure/machine-learning/)

### 实战练习：
- 情感分析模型部署为 Azure 服务
- 使用前端（Streamlit）调用模型接口

---

## ⭐️ 项目模板推荐

| 类型 | GitHub 地址 |
|------|-------------|
| FastAPI + ML 部署框架 | https://github.com/tiangolo/full-stack-fastapi-postgresql |
| Azure ML Pipeline 示例 | https://github.com/Azure/MachineLearningNotebooks |
| Azure MLOps 模板 | https://github.com/microsoft/MLOps |
| Hugging Face 推理笔记本 | https://github.com/huggingface/notebooks/tree/main/examples/inference |

---

## 📘 推荐书籍

- 《Hands-On Machine Learning with Scikit-Learn, Keras and TensorFlow》
- 《Deep Learning with PyTorch》
- 《Designing Machine Learning Systems》

---

## 📌 建议

- 每完成一个阶段，做一次总结推送到 GitHub
- 尝试写博客或知乎分享学习过程
- Azure 云资源成本较高，建议善用免费额度或低配 GPU VM

---

如需 PDF 版本，请使用 Markdown 渲染工具（如 Typora、Obsidian）导出。
