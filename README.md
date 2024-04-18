# FoggyAirsimCityImages

Scene perception is essential for driving-decision making and traffic safety. However, fog, as a kind of common weather, frequently appears in the real world, especially in the mountain areas, making it difficult to accurately observe the surrounding environments. Therefore, precisely estimating the visibility under foggy weather can significantly benefit traffic management and safety.

To facilitate the related research of visibility estimation, a virtual dataset, Foggy Airsim City Images (FACI) is collected using the Airsim simulation platform.

During collection, Version 1.3.1 of AirSim is used on Windows; among the several maps provided by developers, a city scene is chosen; to make the cameras move more freely, the Computer Vision mode is used; and the height and width of the images are set to 576 and 1,024, respectively.

To learn more about the detailed steps of fog synthesis, see the paper [DMRVisNet: Deep Multihead Regression Network for Pixel-Wise Visibility Estimation Under Foggy Weather](https://ieeexplore.ieee.org/document/9794328).

## News:
* 04/18/2024: **The Code of DMRVisNet** has been released on [GitHub](https://github.com/coutyou/DMRVisNet/tree/main).

## Data structure

This repository consists of 100 groups of original data without fog. To generate the complete 3,000  groups of foggy images, you need to run the python script, which is introduced in next section.

The data structure of the dataset is shown below.

```
FoggyAirsimCityImages/
├── 000
│   ├── images
│   │   ├── 0.png
│   │   ├── 1.pfm
│   │   ├── 2.pfm
│   │   ├── 3.png
│   │   ├── 4.pfm
│   │   ├── 5.png
│   │   ├── 6.png
│   │   └── 7.png
│   └── airsim_rec.txt
├── 001
├── 002
├── ...
├── 098
├── 099
└── settings.json
```

The description of each file is shown below.

|   File Name    |                         Description                          |
| :------------: | :----------------------------------------------------------: |
|     0.png      |                      Scene, without fog                      |
|     1.pfm      | DepthPlanar, you get depth in camera plane, i.e., all points that are plane-parallel to the camera have same depth |
|     2.pfm      | DepthPerspective , you get depth from camera using a projection ray that hits that pixel |
|     3.png      |  DepthVis, you get an image that helps depth visualization.  |
|     4.pfm      | DisparityNormalized, disparity image normalized to values between 0 to 1 |
|     5.png      | Segmentation, you get an image that gives you ground truth segmentation of the scene |
|     6.png      |                        SurfaceNormals                        |
|     7.png      |      Infrared, a map from object ID to grey scale 0-255      |
| airsim_rec.txt | The position of multirotor and orientation of camera when data is collected |
| settings.json  |        The settings of AirSim when data is collected         |

To get more information about the data, please refer to [the document of AirSim](https://microsoft.github.io/AirSim/image_apis/).

## How to generate foggy images

### Dependencies

* Python 3.6+
* opencv-python
* imageio
* To read .pfm file via imageio, you need to install the plugin by either
  * the command line script 

    ```
    imageio_download_bin freeimage
    ```

  * the Python method

    ```
    imageio.plugins.freeimage.download()
    ```

### Generation

```python
python generate_pkl.py --input ~/path_to_original_data --output ~/path_to_save_foggy_data
```

For instance,

```python
python generate_pkl.py --input ~/FoggyAirsimCityImages --output ~/data_pkl
```

### Data split

Now, 3,000 groups of foggy data are generated. We divide 3,000 images into training set, validation set, and test set with respect to the ratio of 7:2:1, and the corresponding ranges of  them are shown below.

|    Dataset     |                            Range                             |
| :------------: | :----------------------------------------------------------: |
|  Training set  | The foggy data that generated from original data with No. 000 to No. 069 |
| Validation set | The foggy data that generated from original data with No. 070 to No. 089 |
|    Test set    | The foggy data that generated from original data with No. 090 to No. 099 |

## Citation

Please cite this as:

```
@article{you2022dmrvisnet,
  title={Dmrvisnet: Deep multihead regression network for pixel-wise visibility estimation under foggy weather},
  author={You, Jing and Jia, Shaocheng and Pei, Xin and Yao, Danya},
  journal={IEEE Transactions on Intelligent Transportation Systems},
  volume={23},
  number={11},
  pages={22354--22366},
  year={2022},
  publisher={IEEE}
}
```
