import sys

sys.path.append('/usr/lib/python3/dist-packages')
import cv2
import mediapipe as mp
import numpy as np

# mediapipeの顔ランドマークの初期化
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh()

# 画像を読み込み、RGB形式に変換
# image = cv2.imread("assets/input_1.png")
# image = cv2.imread("assets/input_2.png")
# image = cv2.imread("assets/input_3.png")
# image = cv2.imread("assets/input_4.png")
image = cv2.imread("assets/input_5.png")

if __name__ == "__main__":
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 顔ランドマークの検出を行い、結果を取得
    results = face_mesh.process(image_rgb)

    # 2Dランドマークの座標を取得して、顔の向きを描画
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # 顔の全てのランドマークを描画
            # mp_drawing.draw_landmarks(image, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)

            # ランドマークの座標を取得
            left_eye_left = tuple(map(int, [face_landmarks.landmark[33].x * image.shape[1], face_landmarks.landmark[33].y * image.shape[0]]))
            right_eye_right = tuple(map(int, [face_landmarks.landmark[263].x * image.shape[1], face_landmarks.landmark[263].y * image.shape[0]]))
            # 鼻の頂点のランドマークを取得
            nose_top = tuple(map(int, [face_landmarks.landmark[4].x * image.shape[1], face_landmarks.landmark[4].y * image.shape[0]]))

            # もしランドマーク4が誤検出している場合は、ランドマーク6を使用
            """
            ここでの`20`は、鼻の頂点のランドマーク（`nose_top`）と左目の左端のランドマーク（`face_landmarks.landmark[33]`）のY座標の差の許容範囲を示す。
            具体的には、`nose_top`と`face_landmarks.landmark[33]`のY座標の差が20ピクセル未満であれば、ランドマーク4が誤検出していると判断し、ランドマーク6を`nose_top`として使用する。
            実際の画像やカメラの角度、顔の位置などによって適切な値が変わるので、確認しながら調整する必要あり。
            """
            if abs(nose_top[1] - (face_landmarks.landmark[33].y * image.shape[0])) < 20:  # 20は適切な値に調整
                nose_top = tuple(map(int, [face_landmarks.landmark[6].x * image.shape[1], face_landmarks.landmark[6].y * image.shape[0]]))

            # 鼻筋のランドマークを取得
            if face_landmarks.landmark[1].visibility < 0.5:  # ランドマーク1が見えない場合
                nose_bottom = tuple(map(int, [face_landmarks.landmark[4].x * image.shape[1], face_landmarks.landmark[4].y * image.shape[0]]))
            else:
                nose_bottom = tuple(map(int, [face_landmarks.landmark[1].x * image.shape[1], face_landmarks.landmark[1].y * image.shape[0]]))

            # 各ランドマークの位置に小さな円を描画
            cv2.circle(image, left_eye_left, 5, (0, 0, 255), -1)
            cv2.circle(image, right_eye_right, 5, (0, 0, 255), -1)
            cv2.circle(image, nose_top, 5, (0, 0, 255), -1)

            # 三角形を描画
            triangle_pts = np.array([left_eye_left, right_eye_right, nose_top])
            cv2.polylines(image, [triangle_pts], isClosed=True, color=(0,255,255), thickness=2)

            # 鼻筋の直線を描画
            nose_bottom = tuple(map(int, [face_landmarks.landmark[168].x * image.shape[1], face_landmarks.landmark[168].y * image.shape[0]]))
            cv2.line(image, nose_top, nose_bottom, (0,255,255), 2)

            # 三角形の重心を計算
            centroid = (
                (left_eye_left[0] + right_eye_right[0] + nose_top[0]) / 3,
                (left_eye_left[1] + right_eye_right[1] + nose_top[1]) / 3
            )
            # 三角形の重心と鼻の頂点とのX軸上の距離を計算
            distance_x = nose_top[0] - centroid[0]
            # 矢印の長さを計算（上限を100pxとする）
            arrow_length = min(abs(distance_x), 100) * np.sign(distance_x)  # np.signは符号を取得する関数
            # 矢印の方向ベクトルをX軸に制限
            direction = np.array([arrow_length, 0])

            # 顔の向きを示す矢印を描画
            arrow_end = tuple(map(int, nose_top + direction))
            cv2.arrowedLine(image, nose_top, arrow_end, (255,0,0), 2)

    # 画像を表示
    cv2.imshow("Output", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
