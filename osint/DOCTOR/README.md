Challenge Description

A close friend recently flew to Asia for facial surgery. He told me he found one of the best plastic surgeons, With 26 years of experience

The only problem, He forgot the doctor’s name However, send me this photo from his visit

flag fomrat: SECOPS{Doctor_Full_Name}
example: SECOPS{Kami_Soon-Hom}

![image](image.jpg)

Step 1: Extracting GPS Information
The first step is to use exiftool on the photo to extract metadata.

From the metadata, we find GPS coordinates embedded in the image

exiftool image.jpg
ExifTool Version Number         : 12.76
File Name                       : image.jpg
Directory                       : .
File Size                       : 45 kB
File Modification Date/Time     : 2025:04:20 18:21:39-04:00
File Access Date/Time           : 2025:04:22 11:52:28-04:00
File Inode Change Date/Time     : 2025:04:20 18:21:39-04:00
File Permissions                : -rw-rw-r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Exif Byte Order                 : Big-endian (Motorola, MM)
X Resolution                    : 96
Y Resolution                    : 96
Resolution Unit                 : inches
Y Cb Cr Positioning             : Centered
GPS Version ID                  : 2.3.0.0
GPS Latitude Ref                : North
GPS Longitude Ref               : East
Image Width                     : 724
Image Height                    : 378
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 724x378
Megapixels                      : 0.274
GPS Latitude                    : 37 deg 31' 23.41" N
GPS Longitude                   : 127 deg 1' 40.37" E
GPS Position                    : 37 deg 31' 23.41" N, 127 deg 1' 40.37" E

Step 2: Investigating the Location
We then search the GPS coordinates on Google Maps, and it points us to a place in Asia.

Upon further inspection, we find a clinic named "JK Surgery Clinic" near the location.

Step 3: Finding the Doctor's Name
Now, by googling "JK Surgery Clinic doctors", we find the official website of the clinic.
On the website, there’s a page listing all the doctors.

![doctor](doctor.png)

We search for the doctor who has 26 years of experience.

From the details provided, the doctor's full name is Kim Sung-Sik.

Final Flag

SECOPS{Kim_Sung-Sik}
