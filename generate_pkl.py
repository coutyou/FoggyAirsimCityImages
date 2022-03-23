import os
import imageio
import numpy as np
import pickle
import random
import argparse

import cv2

SKY_COLOR = (210, 226, 73)
SEED = 2021
MAX_DEPTH = 1e6

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def parse_args():
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '-i', '--input',
        type=str,
        help='Path of data to convert. Default: current directory.')
    argparser.add_argument(
        '-o', '--output',
        type=str,
        help='Path where data will be after conversion. Default: data_pkl under current directory.')
    args = argparser.parse_args()

    if not args.input:
        args.input = os.getcwd()
    
    if not args.output:
        args.output = os.path.join(os.getcwd(), "data_pkl")
        
    mkdir(args.output)

    print()
    print("- " + "Params:")
    print(" - Output path: " + str(args.output))
    print(" - Input path:  " + str(args.input))
    print()

    return args

def get_data(args, num_dir, num_img):
    num_str = str(num_dir).zfill(3)
    if num_img in [1,2,4]:
        path = os.path.join(args.input, f"{num_str}", "images", f"{num_img}.pfm")
        img = imageio.imread(path)
        img = np.asarray(img)
        return img
    else:
        path = os.path.join(args.input, f"{num_str}", "images", f"{num_img}.png")
        img = cv2.imread(path)
        if len(img.shape) == 3:
            img = img[:,:,::-1]
        return img

def save_pkl(args, num, idx, data):
    path = os.path.join(args.output, f"{str(num).zfill(3)}_{str(idx).zfill(3)}.pkl")
    with open(path, "wb") as f:
        pickle.dump(data, f)

def gen_A():
    B = random.randint(180, 255)
    G = min(255, B + random.randint(-5, 2))
    R = min(255, (B + G) // 2 + random.randint(-5, 2))
    return np.array([R, G, B]) / 255

def gen_vis():
    return random.randint(1e1, 1e3)

def gen_fog(img, d, A, vis, eps):
    J = img
    beta = -np.log(eps) / vis
    t = np.exp(-beta * d)
    I = J*np.dstack([t]*3) + A*(1-np.dstack([t]*3))
    if I.max() > 1 or I.min() < 0 or t.max() > 1 or t.min() < 0:
        print(I.max(), I.min(), t.max(), t.min())
    return I, t        

def main(args):
    for num in range(100):
        for idx in range(30):
            data = {}
            data["Scene"] = get_data(args, num, 0).astype(float) / 255
    #         data["DepthPlanner"] = get_data(args, num, 1)
            data["DepthPerspective"] = get_data(args, num, 2)
    #         data["DepthVis"] = get_data(args, num, 3)
    #         data["DisparityNormalized"] = get_data(args, num, 4)
    #         data["Segmentation"] = get_data(args, num, 5)
    #         data["SurfaceNormals"] = get_data(args, num, 6)
    #         data["Infrared"] = get_data(args, num, 7)

            data["SkyMask"] = (get_data(args, num, 5) == SKY_COLOR)[:,:,0]
            data["DepthPerspective"] = data["DepthPerspective"] * (1-data["SkyMask"]) + data["SkyMask"] * MAX_DEPTH

            data["A"] = gen_A()
            data["Visibility"] = gen_vis()
            data["FoggyScene_0.05"], data["t_0.05"] = gen_fog(data["Scene"], data["DepthPerspective"], data["A"], data["Visibility"], 0.05)

            save_pkl(args, num, idx, data)
            
    print("DONE.")
    
    
if __name__ == "__main__":
    random.seed(SEED)
    
    args = parse_args()
    
    main(args)
    
    