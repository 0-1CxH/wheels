# chmod +x web_chatgpt
chmod +x del_ds_store
chmod +x gpt_chat


# check WHEELS_PATH is set, if not set to the current path
if [ -z "$WHEELS_PATH" ]; then
    WHEELS_PATH=$(cd "$(dirname "$0")"; pwd)
fi

# add it to the .zshrc
if ! grep -q "WHEELS_PATH" ~/.zshrc; then
    echo "export WHEELS_PATH=$WHEELS_PATH" >> ~/.zshrc
    source ~/.zshrc
    echo "export PATH=$WHEELS_PATH:\$PATH" >> ~/.zshrc
    source ~/.zshrc
fi


# set alias for gpt_chat as gct
if ! grep -q "alias gct" ~/.zshrc; then
    echo "alias gct=$WHEELS_PATH/gpt_chat" >> ~/.zshrc
    source ~/.zshrc
fi

source ~/.zshrc
