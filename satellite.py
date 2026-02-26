import os
import numpy as np
from dotenv import load_dotenv
from sentinelhub import (
    SHConfig,
    BBox,
    CRS,
    SentinelHubRequest,
    DataCollection,
    MimeType
)

# Load environment variables
load_dotenv()

# Get credentials from .env
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Configure Sentinel Hub
config = SHConfig()
config.sh_client_id = CLIENT_ID
config.sh_client_secret = CLIENT_SECRET


def get_ndvi(lat, lon):
    bbox = BBox(
        bbox=[lon - 0.01, lat - 0.01, lon + 0.01, lat + 0.01],
        crs=CRS.WGS84
    )

    evalscript = """
    //VERSION=3
    function setup() {
      return {
        input: ["B04", "B08"],
        output: { bands: 1 }
      };
    }

    function evaluatePixel(sample) {
      let ndvi = (sample.B08 - sample.B04) / (sample.B08 + sample.B04);
      return [ndvi];
    }
    """

    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=("2023-01-01", "2023-12-31"),
            )
        ],
        responses=[
            SentinelHubRequest.output_response("default", MimeType.TIFF)
        ],
        bbox=bbox,
        size=(512, 512),
        config=config,
    )

    response = request.get_data()

    ndvi_array = response[0]
    mean_ndvi = float(np.nanmean(ndvi_array))

    return mean_ndvi