#Hw_1
##Spread Spectrum

###需求:  1. 請根據講義 chapter1-2 的 88-89 頁之演算法,實作一個應用於影像上的程  式,不限定程式語言,隱藏的資訊請以亂數產生,演算法中使用的參數請自 行調整(𝛂以及 spread degree)。 程式輸入:灰階影像、隱藏的資訊(secret message)、演算法相關參數 (parameters)程式輸出:隱藏後的影像(marked image)、隱藏的總資訊量(bit)、取出資訊的正確率(%)。2. 請在規定的時限內將程式以及報告以壓縮檔(不限定格式)方式上傳至 E3,檔名請命名為:Project1_StudentID.rar。3. 報告約一至兩頁,基本資訊包含姓名,學號。報告內文請簡單分析實作結果(必要),實作中遭遇的困難以及解決方式,或 是改善其效果的方法(如沒有則無)。

###實作問題：
1. 隨機產生的***message***與***walk***(pixel探索順序)，若是一樣的情況會造成Sample Pairs Analysis分析隱藏率下降。
2. putpixel會自動檢查overflow或underflow的情況，pixel > 255 則存255，同理則存0