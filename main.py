from parser import parser
import schedule, time, datetime
















if __name__=="__main__":

    schedule.every().day.at("16:37").do(parser)
    print("Ожидание запуска задачи...")
    while True:
        if datetime.datetime.now().day == 11:
            schedule.run_pending()
        time.sleep(30)