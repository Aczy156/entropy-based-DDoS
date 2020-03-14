import json
import config
import pickle


def get_index(date, hour, minute):
    return (minute - config.begin_minute) % config.timeslice + hour - (config.begin_hour) * 3


def data_processing():
    with open(config.data_path) as nginx_data:
        for line in nginx_data:
            record = json.loads(line)
            json_fields = record['_source']['@fields']
            time_json_field = record['_source']['@timestamp']
            # select valid info
            valid_field = ['remote_addr', 'request_method']
            if json_fields[valid_field[1]] == 'GET':
                # print(line)
                # 根据时间添加在特定的位置
                if config.dic.get(json_fields[valid_field[0]]) is None:
                    config.dic[json_fields[valid_field[0]]] = [0] * 5000
                    config.dic.get(json_fields[valid_field[0]])[
                        get_index(int(time_json_field[8:10]), int(time_json_field[11:13]),
                                  int(time_json_field[14:16]))] += 1
                else:
                    config.dic.get(json_fields[valid_field[0]])[
                        get_index(int(time_json_field[8:10]), int(time_json_field[11:13]),
                                  int(time_json_field[14:16]))] += 1
        # for key in config.dic:
        #     print(key)
        #     print(config.dic.get(key))
        dict_file = open(config.pickle_path, 'wb')
        pickle.dump(config.dic, dict_file)


def data_precompute():
    # extract valid data
    keys = list(config.dic.keys())
    for key in keys:
        is_positive = 0
        is_remove = True
        for i in config.dic[key]:
            if i > 0:
                is_positive += 1
                if is_positive >= 10:
                    is_remove = False
            else:
                is_positive = 0
        if is_remove:
            del config.dic[key]
        # if is_positive < 10:
        #
        #     # config.dic.pop(key)
        #     del config.dic[key]
        #     continue
    for key in config.dic.keys():
        print(key)
        print(config.dic.get(key))
    # for i in config.dic:


# compute entropy


#     config.

if __name__ == '__main__':
    # data_processing()
    out_file = open(config.pickle_path, 'rb')
    config.dic = pickle.load(out_file)
    data_precompute()
