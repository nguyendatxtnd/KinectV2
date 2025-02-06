1. Cài đặt libfreenect2
- libfreenect2 là thư viện mã nguồn mở dùng để giao tiếp với kinect v2 mà không cần SDK.
- Cài đặt các phụ thuộc cần thiết:

        sudo apt update
        
        sudo apt-get install build-essential cmake pkg-config -y

        sudo apt-get install libusb-1.0-0-dev libturbojpeg0-dev libglfw3-dev -y

        sudo apt-get install libglew-dev libglm-dev -y

        sudo apt-get install libva-dev libjpeg-dev -y

        sudo apt-get install libopenni2-dev -y


    
- cài đặt libfreenect2 từ GitHub:

        git clone https://github.com/OpenKinect/libfreenect2.git

        cd libfreenect2

        mkdir build && cd build

        cmake ..

        make

        sudo make install

- Kiểm tra cài đặt:

            cd ~/libfreenect2/build/bin

            ./Protonect

2. Cài đặt pylibfreenect2
- pylibfreenect2 là binding python của thư viện libfreenect2 (dành cho kinect v2).

        https://r9y9.github.io/pylibfreenect2/latest/installation.html

2. 
- lưu ý: dữ liệu thu được từ đoạn file code sau chưa có sự đồng nhất về kích thước của 2 dữ liệu depth và rgb (depth: 512x424, rgb: 1920x1080 )

- Tạo folder để lưu dữ liệu (chú ý sửa tên các folder trong code (data/data_test (or data/data_train) và file data/data_test.csv (or data/data_train.csv (folder trong code)) để lưu dữ liệu và đường dẫn đến file lưu dữ liệu))

- Sau khi cài đặt xong các thư viện và tạo các file, folder thì chạy file connectAndgetdataKinectV2.py:

        python3 connectAndgetdataKinectV2.py

- Dữ liệu thu được sẽ lưu ở trong foder data đã tạo ở trên.
- 


4. Một số lỗi có thể gặp phải:

- Nếu gặp lỗi liên quan đến VA-API khi xử lí với GPU thì thêm đường dẫn sau vào terminal trước khi chạy file:

        export LIBVA_DRIVER_NAME=nvidia

  Hoặc thêm dòng sau vào đoạn đầu code sau khi đã khai báo thư viện:

        os.environ["LIBVA_DRIVER_NAME"] = "nvidia"

- Nếu bị treo tại hàm frames = listener.waitForNewFrame() thì có thể phần cứng đang gặp lỗi.









            
