SOURCE="./"
TARGET="pi@10.0.0.98:/home/pi/python_programs/pi-cal"
EXCLUDE=(
    "/*"
    "__pycache__"
    "token.json"
)
INCLUDE=(
    "credentials.json"
    "pi-cal.py"
    "requirements.txt"
    "src"
)


for i in "${!EXCLUDE[@]}"
do
    EXCLUDE[i]="--exclude=${EXCLUDE[i]}"
done

for i in "${!INCLUDE[@]}"
do
    INCLUDE[i]="--include=${INCLUDE[i]}"
done

rsync -avr --delete "${INCLUDE[@]}" "${EXCLUDE[@]}" "${SOURCE}" "${TARGET}"