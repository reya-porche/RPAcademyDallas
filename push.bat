@echo off
echo Committing and pushing changes...
git add .
git commit -m "Auto commit: %date% %time%"
git push origin main
echo Done!