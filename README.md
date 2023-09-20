

![](https://raw.githubusercontent.com/yKesamaru/Estimate_face_orientation/master/assets/eye_catch.png)

- [はじめに](#はじめに)
- [アルゴリズム](#アルゴリズム)
- [実装](#実装)
- [出力結果](#出力結果)

## はじめに

頭部姿勢推定は、顔の向きや角度を計算する技術です。
この記事では、**複雑なパラメーターを使用せず**、簡易的な方法を用いて頭部姿勢を推定する方法を紹介します。具体的には、顔のランドマークを利用して三角形をつくり、その重心から顔の向きを2D平面上で推定します。
![](https://raw.githubusercontent.com/yKesamaru/Estimate_face_orientation/master/assets/head_estimation.png)



通常、頭部姿勢推定にはカメラの
- 内部パラメーター
- 外部パラメーター

が必要となります。内部パラメーターは、カメラの焦点距離や画像の中心点などを表すパラメーターで、カメラごとに異なります。外部パラメーターは、カメラ座標系とワールド座標系との間の変換を示すパラメーターで、カメラの位置や向きに応じて変化します。

これらのパラメーターを用いて、以下のような図が得られます。
![](https://raw.githubusercontent.com/yKesamaru/Estimate_face_orientation/master/assets/pose_2.jpg)
- [opencv/Pose Estimation](https://docs.opencv.org/4.x/d7/d53/tutorial_py_pose.html)

あるいは[こちらのリポジトリ](https://github.com/yinguobing/head-pose-estimation)では、深層学習を用いて頭部姿勢を推定する方法も紹介されています。

![](https://raw.githubusercontent.com/yinguobing/head-pose-estimation/master/doc/demo.gif)

しかしながら実際は、これらのパラメーターを正確に求めようとすると大変です。また、深層学習を用いた方法は、計算量が多くなってしまいます。

この記事では、これらの複雑なパラメーターを使用せず、簡易的な方法を用いて頭部姿勢を推定する方法を紹介します。
顔のランドマークを利用して三角形をつくり、その重心から顔の向きを2D平面上で推定します。

## アルゴリズム
1. **両目を結ぶ直線の分析**
   - この直線が水平に近い場合、顔は正面を向いている可能性が高い。
   - この直線が傾いている場合、顔が左右に傾いている可能性がある。この傾きの度合いは、顔の傾きの度合いを示す。

2. **左目、右目、鼻の頂点を結ぶ三角形の分析**
   - 三角形の形状や大きさを分析することで、顔の向きを推定。
   - 三角形の重心と鼻の頂点の位置関係を分析することで、顔の左右の向きを推定。

3. **鼻筋の直線の分析**
   - この直線の長さや位置を分析することで、顔が上下に傾いているかを推定。
   - 鼻筋の直線が三角形の底辺の中央を通る場合、顔は正面を向いていると推定。
   - 鼻筋の直線が三角形の底辺の左側を通る場合、顔は左に向いていると推定。
   - 鼻筋の直線が三角形の底辺の右側を通る場合、顔は右に向いていると推定。

## 実装

https://github.com/yKesamaru/Estimate_face_orientation/blob/66fc101a43cbac3e42f4ff7d74647fb2e453463c/head_estimation.py#L1-L85


顔の向きがきつい時、一部のランドマークが検出できない可能性があります。そのため、コード中ではいくつかのランドマークを選びなおせるようにしています。


## 出力結果
見にくいですが、青の矢印が顔の向きを表しています。
顔の向きがきついほど、矢印の長さが長くなります。（上限100px）

![](https://raw.githubusercontent.com/yKesamaru/Estimate_face_orientation/master/assets/head_estimation.png)


実際に使用する時は、このような描画は必要ないので、**極めて高速な動作が期待されます**。
デメリットとして、完全に左右を向いてしまうと、顔の向きを推定できなくなってしまいます。あまり厳密に推定する必要がない場合は、この方法を用いることで、簡易的に頭部姿勢を推定できます。

以上です。ありがとうございました。