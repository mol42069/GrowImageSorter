
import os, math, shutil
import datetime as dt


def rename(path):               # from earlier script

    dicti = {}
    lastName = ""
    oldFiles = []
    counter = 0

    for filename in os.listdir(path):
        if filename[4] == "-":
            oldFiles.append(filename)
            continue

    for i, filename in enumerate(os.listdir(path)):

        if not filename in oldFiles:

            tempName = filename.split('_')[0]
            finalName = ""

            for x, letter in enumerate(tempName):

                if x == 4:
                    finalName += "-" + letter
                elif x == 6:
                    finalName += "-" + letter
                else:
                    finalName += letter

        else:
            finalName = filename.split('.')[0]
            if finalName[-2] == "#":
                counter = int(finalName[-1])
                finalName = finalName.split("#")[0]

        if lastName == finalName or lastName == finalName + "#" + str(counter):
            counter += 1
            finalName += "#" + str(counter)

        temp1 = finalName + ".jpg"
        temp2 = finalName + "#" + str(counter) + ".jpg"

        if (temp1 in oldFiles and counter == 0) or temp2 in oldFiles:

            counter += 1
            temp3 = finalName + "#" + str(counter) + ".jpg"
            if temp3 in oldFiles:
                while finalName + "#" + str(counter) + ".jpg" in oldFiles:
                    counter += 1

            finalName += "#" + str(counter)

        else:
            counter = 0

        dicti.update({finalName: filename})
        lastName = finalName

    for newName in dicti.keys():

        src = path + "/" + dicti[newName]
        dest = path + "/" + newName + ".jpg"
        os.rename(src, dest)






def main():

    path = input("ENTER THE FOLDER: ")
    firstDay = None
    rename(path + "/INPUT")

    FirstEntry = True
    count = 0

    for (root, dirs, file) in os.walk(path):    # we get all files/folders in this directory
        print(dirs)
        print(file)
        if len(dirs) <= 1 and FirstEntry:                      # here we know this is the first week.

            print("first entry")
            if len(file) > 0:
                date = file[0].split('.')[0].split('#')[0].split('-')
                firstDay = dt.datetime(int(date[0]), int(date[1]), int(date[2]))



        elif len(dirs) > 1:                                   # here we know it isn't the first week

            FirstEntry = False
            print("not new")

        elif len(file) > 0:                                   # here we get the files

            if count == 1:                                    # we make sure we use the images from "INPUT"
                date = file[0].split('.')[0].split('#')[0].split('-')
                firstDay = dt.datetime(int(date[0]), int(date[1]), int(date[2]))
            count += 1


    if firstDay is None:

        print("there is no picture!")

        exit(-1)

    else:

        sort_img(path, firstDay)



    return


def sort_img(path, firstDay):

    src_path = path + "/INPUT"
    files = os.listdir(src_path)

    directs = None
    for (root, dirs, file) in os.walk(path):        # we create an array with all directorys in our folder
        if len(dirs) > 0:
            directs = dirs

    print("dirs: ")
    print(directs)

    for file in files:                              # we get the date of a file and calculate the time difference
        date = file.split('.')[0].split('#')[0].split('-')         # this image and the first image.
        thisDay = dt.datetime(int(date[0]), int(date[1]), int(date[2]))

        timeDif = thisDay - firstDay

        # then now we reassemble the name with the day included.

        temp = file.split('.')[0].split('#')

        if len(temp) == 1:

            nName = temp[0] + '-D' + str(timeDif.days + 1) + ".jpg"
        else:

            nName = temp[0] + '-D' + str(timeDif.days + 1) + '#' + temp[1] + ".jpg"


        # here we calculate in which week the image is taken

        week = "Week " + str(math.ceil(timeDif.days/7) + 1)

        if week in directs:     # we check if the week already exists and if the image already exists in that week
            imgs = os.listdir(path + "/" + week)
            if nName not in imgs:                   # if the image doesent exists yet we copy the image here.

                # copy the image and then remove the image from the "INPUT" folder

                src_temp = src_path + "/" + file
                dest_temp = path + "/" + str(week) + "/" + nName
                shutil.copy(src_temp, dest_temp)
                os.remove(src_temp)

                pass


        else:                   # and if the week doesent exist yet we create the folder and copy the images over.

            # create a folder, copy the image and then remove the image from the "INPUT" folder:

            os.mkdir(path + "/" + str(week))
            src_temp = src_path + "/" + file
            dest_temp = path + "/" + str(week) + "/" + nName
            shutil.copy(src_temp, dest_temp)
            directs.append(week)
            os.remove(src_temp)

    return





if __name__ == '__main__':
    main()