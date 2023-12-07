import aspose
import apose.threed
from aspose.threed import FileFormat
scene = aspose.threed.Scene.from_file("Frog.usdz")
scene.save("Frog.obj", aspose.threed.FileFormat.WAVEFRONT_OBJ)
