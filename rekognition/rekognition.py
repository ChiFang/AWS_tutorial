import pprint
import os
import time
import boto3

# Set this to whatever percentage of 'similarity'
# you'd want
SIMILARITY_THRESHOLD = 0.0

LOG_RAW = False # True

LOG_OUTPUT_IMAGE = True

if __name__ == '__main__':

    SourceFile = 'src.jpg'
    TargetFile = 'tar.jpg'
    
    
    # Read credentials from the environment
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    print "my ACCESS_KEY_ID: " + access_key
    print "my SECRET_ACCESS_KEY: " + secret_key
    
    region = 'us-east-1' # So support is only available in us-east-1 right now on Aug 13 2016
    
    if access_key is None or secret_key is None:
        print('No access key is available.')
        sys.exit()

    print "Set client..."
    client = boto3.client('rekognition',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region)
    

    print "Set source img..."
    with open(SourceFile, 'rb') as source_image:
        source_bytes = source_image.read()

    print "Set target img..."
    with open(TargetFile, 'rb') as target_image:
        target_bytes = target_image.read()

    print "compare_faces..."
    tStart = time.time()
    response = client.compare_faces(
                   SourceImage={ 'Bytes': source_bytes },
                   TargetImage={ 'Bytes': target_bytes },
                   SimilarityThreshold=SIMILARITY_THRESHOLD
    )
    tEnd = time.time()
    print "It cost %f sec for faces compare~~~" % (tEnd - tStart)
    
    print "print result..."
    
    pprint.pprint(response)
    
    text_file_1 = open("log.txt", "w")
    pprint.pprint(response, text_file_1)
    text_file_1.close()
    
    print("------------\n")
    print("Seg Result")
    print len(response)
    pprint.pprint(response['FaceMatches'])
    print("------------\n")
    FaceNum = len(response['FaceMatches'])
    print("there are " + str(FaceNum) + " faces")
    
    print("------------\n")
    
    if LOG_OUTPUT_IMAGE == True:
        from PIL import Image, ImageDraw, ImageFont
        source_img = Image.open( TargetFile )
        ImgWidth, ImgHeight = source_img.size
        # ImgWidth = source_img.get_width()
        # ImgHeight = source_img.get_height()
        
    
    
    for index in range(FaceNum):
        #print response['FaceMatches'][index]['Face']
        print "Face " + str(index) + ":"
        print "Similarity:" + str(response['FaceMatches'][index]['Similarity'])
        print "BoundingBox:" + str(response['FaceMatches'][index]['Face']['BoundingBox'])
        Left = int(ImgWidth*response['FaceMatches'][index]['Face']['BoundingBox']['Left'])
        Top = int(ImgHeight*response['FaceMatches'][index]['Face']['BoundingBox']['Top'])
        Width = int(ImgWidth*response['FaceMatches'][index]['Face']['BoundingBox']['Width'])
        Height = int(ImgHeight*response['FaceMatches'][index]['Face']['BoundingBox']['Height'])
        Similarity = response['FaceMatches'][index]['Similarity']
        
        print Left, Top, Width, Height
        if LOG_OUTPUT_IMAGE == True:
            draw = ImageDraw.Draw(source_img)
            draw.rectangle(((Left, Top), (Left+Width, Top+Height)), outline='red')
            draw.text((Left, Top), str(Similarity), font=ImageFont.truetype("arial", 24))
            # draw.rectangle(((350, 300), (450, 400)), outline='red')
            # draw.text((350, 300), str(Similarity), font=ImageFont.truetype("arial", 16))
            
    if LOG_OUTPUT_IMAGE == True:
        # You can save where ever you want
        source_img.save( "FacesCompare_Out.png")
    
 
    
    if LOG_RAW == True:
        print("------------\n")
        print("Raw Result")
        print (response)
        text_file = open("log_raw.txt", "w")
        text_file.write(str(response))
        text_file.close()