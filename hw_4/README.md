#Hw_4
##Trellis code and linear correlation

###需求:  請實作一個利用 trellis code 嵌入 8 bits 的 linear correlation 方法,詳細需求   
1. 嵌入的資訊分別為:0、255、101、154、128、127 以及不藏任何資訊。  2. Pattern 的大小為 8 by 8,因此影像也是以 8 by 8 的 block 來嵌入。  3. Trellis code 需加入 2 bits (00),因此一共是 10 bits,方法如講義  4.  請輸出結果曲線圖,如講義 ch04_elg7173-new 的 p.52。  5. 整體的流程可以參考講義 ch04_elg7173-new 的 p.47-52。  

###遭遇困難

1. 隱藏message128後再分析上都會找出不正確的其他路徑。  
2. 分佈沒有依照 gauss unit variance 在尋找路徑上會有些微影響。
3. 從圖片取出來的pixel並沒有屬於gauss分佈，若用該vector會找不到正確路徑。

###解決方式

1. 取高斯數值的時候做round，減少後面取整產生比較大的誤差，可以準確找出128
2. 調整gauss參數，符合standard gauss即可。
3. 需要扣掉向量平均。


###實驗結果
![Analysis Result](./linear_correlation.png)