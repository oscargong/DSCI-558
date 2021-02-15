# DSCI 558 HW7 Report


## Task 2: Knowledge Graph Embeddings

### Task 2.1

#### TransE

![TransE eval.png](https://i.loli.net/2020/11/11/kNcLgWxA4lPsJKS.png)

![TransE.png](https://i.loli.net/2020/11/11/GrFNBlY9H5yR3K2.png)

#### DistMult

<img src="https://i.loli.net/2020/11/11/TgU9nWwXk4tlohB.png" alt="DistMult evl.png" style="zoom: 50%;" />

<img src="https://i.loli.net/2020/11/11/VvF6gyNRqGBnc83.png" alt="DistMult.png" style="zoom: 50%;" />

#### ComplEx

![CleanShot 2020-10-23 at 19.35.59@2x.png](https://i.loli.net/2020/10/24/ONUrilZxPG27MbT.png)

![ComplEx.png](https://i.loli.net/2020/11/11/6DsawfemLdOGl9F.png)

### Task 2.2

We've already know that TransE cannot represent one-to-many relationship, DistMult cannot model asymmetric relations, and ComplEx allows asymmetry. There are lots of one-to-many relationship in this task. Therefore the overall perfornamce of TransE is not really good.

Those different models yield different embedding vectors, and have different scoring functions.

The plot of DistMult and ComplEx are similar since thee ComplEx model is an extension of the DistMult model, and their scoring functions are similar as well.

Comparing the plot of TransE with DisMult and Complex, its spot are sparser, thus, its MMR goes down.

