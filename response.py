def respond_to_intrusion(results):
    if any(results):
        print("检测到入侵行为，采取相应措施！")
        # 这里可以添加更具体的响应逻辑，如报警、阻断网络连接等
    else:
        print("未检测到入侵行为。")