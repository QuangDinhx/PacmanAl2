# PacmanAl2

## Problem Search

### Q1:  Reflex Agent
  Bài này ta sẽ dùng một hàm để đánh giá độ ưu tiên giữa các bước đi của pacman dựa trên khoảng 
  cách giữa của pacman tới food và khoảng cách với những con ma tù đó đưa ra số điểm đánh giá 
  tương ứng
  Sự đánh giá này được diễn tả bởi như sau:   
    - Với mỗi thức ăn thì ta tìm khoảng cách ngắn nhất từ pacman tới thức ăn gần nhất thì ta trừ nó với số điểm hiện tại
    - Với mỗi con ma thì ta tìm khoảng cách ngắn nhất từ pacman tới con ma gần nhất thì ta cộng nó với số điểm hiện tại
    - Với mỗi lúc khoảng cách giữa pacman với ma ngắn hơn hoặc bằng một thì trả về -inf để loại trừ luôn bước đi đó
### Q2:  
