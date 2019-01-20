key = "AIzaSyAg_4PkGkqPff1fIy0P2HbnHbewR-bFsKs"

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

client = vision.ImageAnnotatorClient()

'''def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of Face objects with information about the picture.
    """
    client = vision.ImageAnnotatorClient()

    response = client.annotate_image({
    'image': {'source': {'imageUri'}}
  "faceAnnotations": [
    {
      object(FaceAnnotation)
    }
  ]})
        

    
    final_content = open(face_file, 'rb')
    content = final_content.read()
    image = types.Image(content=content)

    #return client.face_detection(image=image, max_results=max_results).face_annotations
    return response

'''
def detect_face(path):
    """Detects faces in an image."""
   
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    """for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        print('sorrow: {}'.format(likelihood_name[face.sorrow_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))"""
    if len(faces) == 0:
        return ['UNKNOWN','UNKNOWN','UNKNOWN','UNKNOWN']
    face = faces[0]
    return [likelihood_name[face.anger_likelihood], likelihood_name[face.joy_likelihood], likelihood_name[face.surprise_likelihood], likelihood_name[face.sorrow_likelihood]]

def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    # Sepecify the font-family and the font-size
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y - 30),
                  str(format(face.detection_confidence, '.3f')) + '%',
                  fill='#FF0000')
    im.save(output_filename)

def main(input_filename):
    faces = detect_face(input_filename)
    print('Found {} face{}'.format(len(faces), '' if len(faces) == 1 else 's'))

        #print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
        #image.seek(0)
        #highlight_faces(image, faces, output_filename)
#if __name__ == "__main__":
#    main('happy.png')
