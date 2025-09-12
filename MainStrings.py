import subprocess

Models = [
    "hf.co/RCDWealth/Dolphin3.0-Qwen2.5-1.5B-Q5_K_M.gguf:latest",
    "https://huggingface.co/nold/FuseChat-7B-VaRM-GGUF",
    "https://hf.co/bartowski/Llama-3.2-3B-Instruct-uncensored-GGUF:F16",
    "https://huggingface.co/NousResearch/Nous-Hermes-2-Mistral-7B-DPO-GGUF"
]

ExitCommands = {"!exit", "!quit"}

ReadyText = "AI Assistant has finished initializing!\nType \"!Exit\" to leave."
UserPrompt = "HUMAN: "
AiName = "Kori"
UserName = subprocess.run("whoami", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=15)

ResponsePersonallity = (
    f"You, the AI, are {AiName}. ",
    f"{AiName} is responsible for answering the HUMAN, otherwise known as {UserName}, with the relevant information. ",
    f"{AiName} is cheerful, but mostly direct. {AiName} doesn't attempt to make the truth easier, but remains happy."
)

LogicPersonallity = (
    #shit here again
)

DirectPersonallity = (
    #shit here
)
