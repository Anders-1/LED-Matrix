import cv2

img = cv2.imread('C:/Users/ahpye/Desktop/dev/LED_Matrix_Spotify_API_WIP/img2.jpg')
res = cv2.resize(img, dsize=(32, 32), interpolation=cv2.INTER_CUBIC)
cv2.imwrite('C:/Users/ahpye/Desktop/dev/LED_Matrix_Spotify_API_WIP/img2.bmp', res) 