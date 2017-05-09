import pprint
import os
import time
import boto3

# Set this to whatever percentage of 'similarity'
# you'd want
SIMILARITY_THRESHOLD = 75.0

if __name__ == '__main__':
    
    # Read credentials from the environment
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    print "my ACCESS_KEY_ID: " + access_key
    print "my SECRET_ACCESS_KEY: " + secret_key
    
    region = 'us-east-1'
    
    if access_key is None or secret_key is None:
        print('No access key is available.')
        sys.exit()

    print "Set client..."
    client = boto3.client('rekognition',
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region)
    

    print "Set source img..."
    # Our source image: http://i.imgur.com/OK8aDRq.jpg
    with open('src.jpg', 'rb') as source_image:
        source_bytes = source_image.read()

    print "Set target img..."
    # Our target image: http://i.imgur.com/Xchqm1r.jpg
    with open('tar.jpg', 'rb') as target_image:
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
    print("Raw Result")
    print (response)

    
    text_file = open("log_raw.txt", "w")
    text_file.write(str(response))
    text_file.close()