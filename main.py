import argparse
import datetime
import os
import warnings
warnings.filterwarnings("ignore")

import pandas as pd

from traffic_video_analytics.processor import Processor
from traffic_video_analytics.const import DEFAULT_INPUT_VIDEOS, DEFAULT_OUTPUT_DIR, DEFAULT_PROCESSING_INTERVAL


if __name__ == "__main__":

    # let us put path videos and output dir as arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_videos", type=str, default=DEFAULT_INPUT_VIDEOS)
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--processing_interval", type=float, default=DEFAULT_PROCESSING_INTERVAL)

    args = parser.parse_args()
    path_videos = args.path_videos
    output_dir = args.output_dir
    processing_interval = args.processing_interval

    if output_dir == None:
        output_dir = f"./outputs/{datetime.datetime.now().strftime('%Y-%m-%d/%H-%M-%S')}"

    print(f"Processing videos from {path_videos}")

    output_tables = []
    processor = Processor()
    for video in os.listdir(path_videos):
        print(f"Processing video: {video}")
        results = processor.one_video_run(
            os.path.join(path_videos, video),
            processing_interval, output_dir
        )
        output_tables.append(results)

    table = pd.concat(output_tables)
    table.to_csv(f"{output_dir}/results.csv", index=False)
    print(f"Results saved to {output_dir}/results.csv")
