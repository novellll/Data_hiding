#Hw_2
##LSB_Replacement
###需求:  1. 請根據講義 Lecture02 的 21-26 頁之演算法實作程式,分析以LSB replacement(11-13 頁)方法藏入資訊的附檔灰階影像。隱 藏的資訊以亂數產生,隱藏的資訊量為該影像總像數的 5%、 25%以及 50%。不限定程式語言。

##Sample Analysis  
* 輸出分別用LSB與StM隱藏機密資訊的結果圖。
	 
##Stochastic Modulation  
* 利用高斯分佈產生的r與s，藉由parity function計算與隱藏機密資訊的值相同並將r或s加入該pixel，**可能會造成overflow**因此需要運算boundary來判斷。

###實作問題：
1. 隨機產生的***message***與***walk***(pixel探索順序)，若是一樣的情況會造成Sample Pairs Analysis分析隱藏率下降。
2. putpixel會自動檢查overflow或underflow的情況，pixel > 255 則存255，同理則存0
3. parity function的i代表區間而非index，用來判斷x得值介於第幾個k的區間。