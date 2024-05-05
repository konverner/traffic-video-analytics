## Traffic Video Analytics

A package for vehicle identification system.

## Get started

### Installation

1. Clone repository
```bash
git clone 
```

2. Install the package

```bash
pip install .
```

3.1. Run as a script

```bash
python main.py --input <input_videos_path> --processing_interval <processing_interval>
```

3.2. Run as a package

```python
from traffic_video_analytics.processor import Processor

processing_interval = 0.2
video_path = "./inputs/test1.mp4"
processor = Processor()

processor.one_video_run(video_path, processing_interval)
```