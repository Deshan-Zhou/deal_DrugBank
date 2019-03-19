# deal_DrugBank
在这个程序里面，我用Python的xml.sax库来提取xml文件里面的某些数据。
比如药物DrugBank id；药物名称；药物对应的ChEMBL id；药物与药物之间有影响作用的药物DrugBank id；药物作用的靶标id等。
此xml文件的数据具有数据量较大，且便签命名有很多重复等特点（比如有多个name，id）。如何比较准确提取出我想要的上述信息是一个需要思考的地方
