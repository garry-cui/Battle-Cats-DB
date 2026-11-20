#!/bin/bash

#Congifuration
PACKAGE="jp.co.ponos.battlecatsen"
MAIN_PATH="./apks/en"


# Dependencies
echo "Checking dependencies..."

if ! command -v java >/dev/null 2>&1; then
    echo "ERROR: Java is not installed or not in PATH."
    exit 1
fi

if ! command adb version >/dev/null 2>&1; then
    echo "ERROR: ADB is not installed or not in PATH"
    exit 1
fi


# Check phone connection
echo "Checking Andriod phone connection..."

DEVICE_COUNT=$(adb devices | awk '$2 == "device" { count++ } END { print count+0 }')

if [ "$DEVICE_COUNT" -ne 1 ]; then
    echo "ERROR: Expected exactly one authorised phone."
    adb devices
    exit 1
fi


# Find game version
echo "Finding Battle Cats package info..."

if ! command adb shell pm path "$PACKAGE" >/dev/null 2>&1; then
    echo "ERROR: Battle Cats could not be found on the device."
    exit 1
fi

VERSION_NAME=$(adb shell dumpsys package "$PACKAGE" | findstr versionName)
VERSION_NUMBER="${VERSION_NAME#*=}"

echo "Detected version: $VERSION_NUMBER"


# Pulling split APKs
echo "Pulling APKs..."

APK_PATHS=$(adb shell pm path "$PACKAGE")

while IFS= read -r LINE; do

    LINE=${LINE%$'\r'}
    APK_PATH="${LINE#package:}"
    echo "$APK_PATH"

    MSYS_NO_PATHCONV=1 adb pull "$APK_PATH" "$MAIN_PATH"

done <<< "$APK_PATHS"

# Merging APK using APKEditor
echo "Merging split APKs into single APK..."

FILE_NAME="Battle_Cats_en_$VERSION_NUMBER.apk"

java -jar "./lib/APKEditor-1.4.9.Jar" m -i "$MAIN_PATH" -o "$MAIN_PATH/$FILE_NAME"

find "$MAIN_PATH" -type f -name "*.apk" ! -name "$FILE_NAME" -delete


MERGE_APK_PATH="$MAIN_PATH/$FILE_NAME"
OUTPUT_PATH="$MAIN_PATH/v$VERSION_NUMBER"


echo ""
echo ""
echo "Successfully pulled Battle Cats game file version $VERSION_NUMBER!"

python3 "./src/extraction/extract_apk.py" "$MERGE_APK_PATH" "$OUTPUT_PATH"

python3 "./src/decoding/decrypt.py" "$VERSION_NUMBER"
