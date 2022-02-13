# -*- coding cp-1252 -*-
import time
# import sys
from bit import Key
import os
from bit.format import bytes_to_wif
from multiprocessing import Lock, Process, cpu_count

def get_babulesy(numpotok, k_count, profit_file, base_file, lock):
    pid = os.getpid()
    lock.acquire()
    print("PID process", pid, numpotok, ' read base as file...', flush=True)
    start = time.time()
    t = frozenset([line.rstrip('\n') for line in open(base_file, 'r',
                                                      encoding="cp1252")])  # Кодирование из СУЩЕСТВУЮЩЕЙ базы из формата txt, которую вы нашли
    print('time read(sec): ', time.time() - start, flush=True,)
    del (start)
    lock.release()
    y = 0
    print("PID process", pid, numpotok, 'start generation...', flush=True)
    while True:
        # генерация ключей
        y += 1
        print("PID process", pid, numpotok, 'generation ', y, flush=True)
        mass = {}
        for _ in range(k_count):
            k = Key()  # сжатие ключей
            
            wif = bytes_to_wif(k.to_bytes(), compressed=False)  # распаковка ключей
            k1 = Key(wif)  # добавление адреса с ключем
            mass[k1.address] = wif

        # проверка адреса
        print("PID process", pid, numpotok, 'verification ...', y, flush=True)
        vall_set = set(mass.keys())
        c = vall_set.intersection(t)
        if c:
            print("PPID process!!!!!!!!!!!!!!!!!", pid, numpotok, 'WIIINNNNN!!! ...', flush=True)
            with open(profit_file, 'a') as out:
                for gg in c:
                    out.write('{},{}\n'.format(gg, mass[gg]))
                out.close()


if __name__ == '__main__':
    key_count = 100000
    pat = os.path.dirname(__file__)
    baseName = pat + 'base.txt'
    profit = pat + 'out.txt'

    lock = Lock()

    procs = []
    for u in range(6):  # параметры запуска для 6 ядер и 25Гб оперативной памяти
        proc = Process(target=get_babulesy, args=(u, key_count, profit, baseName, lock))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
