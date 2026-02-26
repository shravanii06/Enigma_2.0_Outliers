import os
import numpy as np
from dotenv import load_dotenv
from datetime import date, timedelta

from sentinelhub import (
    SHConfig,
    BBox,
    CRS,
    SentinelHubRequest,
    DataCollection,
    MimeType
)

# -----------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------
load_dotenv()

CLIENT_ID="92453595-3496-45ed-9d8d-9c4d4476f299"
CLIENT_SECRET="x0aCifSnSKC2iWj6vtmEWj8dlZhPb0cQ"
print("CLIENT_ID:", CLIENT_ID)
print("CLIENT_SECRET:", CLIENT_SECRET)

# -----------------------------
# CONFIGURE SENTINEL HUB
# -----------------------------
config = SHConfig()
config.sh_client_id = CLIENT_ID
config.sh_client_secret = CLIENT_SECRET


def get_ndvi(lat, lon):
    """
    Fetch NDVI value for given latitude and longitude.
    Returns mean NDVI between -1 and +1.
    """

    try:
        # Define small bounding box around the point
        bbox = BBox(
            bbox=[lon - 0.01, lat - 0.01, lon + 0.01, lat + 0.01],
            crs=CRS.WGS84
        )

        # Use last 30 days data
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        evalscript = """
        //VERSION=3
        function setup() {
          return {
            input: [{
                bands: ["B04", "B08"],
                units: "REFLECTANCE"
            }],
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
                    time_interval=(str(start_date), str(end_date)),
                    mosaicking_order="leastCC"
                )
            ],
            responses=[
                SentinelHubRequest.output_response("default", MimeType.TIFF)
            ],
            bbox=bbox,
            size=(256, 256),
            config=config,
        )

        response = request.get_data()

        if not response:
            return None

        ndvi_array = response[0]

        ndvi_array = np.where(ndvi_array == 0, np.nan, ndvi_array)

        mean_ndvi = float(np.nanmean(ndvi_array))

        if mean_ndvi > 1:
           mean_ndvi = mean_ndvi / 100

        return round(mean_ndvi, 3)

    except Exception as e:
        print("NDVI Error:", e)
        return None