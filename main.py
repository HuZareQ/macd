import pandas as pd
import matplotlib.pyplot as plt

def printGraph(vector, macd, signal, capital):
    # Wykres ceny
    plt.plot(vector)
    plt.title('Wykres ceny')
    plt.xlabel('Numer próbki')
    plt.ylabel('Cena')

    # Wykres MACD
    plt.figure()
    plt.plot(macd)
    plt.plot(signal)
    plt.title('Wykres MACD i sygnału')
    plt.xlabel('Numer próbki')
    plt.ylabel('Wartość')
    plt.legend(['MACD', 'Signal'])

    # Wykres ceny
    plt.figure()
    plt.plot(capital)
    plt.title('Wykres dostępnych środków')
    plt.xlabel('Numer próbki')
    plt.ylabel('Kwota')

    plt.show()

def CalcEMA(vector, day, count):
    alpha = 2 / (count + 1)
    nominator = 0.0
    denominator = 0.0
    for i in range(count):
        tmp = (1 - alpha) ** i
        if day - i > 0:
            nominator += tmp * vector[day - i - 1]
        else:
            nominator += tmp * vector[0]
        denominator += tmp
    return nominator / denominator

def buy_shares(capital, price, shares):
    available_shares = int(capital / price)
    if available_shares > 0:
        shares += available_shares
        capital -= available_shares * price
    return capital, shares

def sell_shares(capital, price, shares):

    capital += shares * price
    shares = 0
    return capital, shares

def main():
    tmp = pd.read_csv('Projekt_Mbank.csv', header =  0 , sep = ',')
    tmp2 = tmp['Maks.']
    prices = list(reversed(tmp2))

    macd = [0.0] * len(prices)
    signal = [0.0] * len(prices)
    capital = 1000
    capitalTab = [0.0] * len(prices)
    capitalSell = []
    shares = 0
    for day in range(len(prices)):
        #create macd and signal
        macd[day] = CalcEMA(prices, day, 12) - CalcEMA(prices, day, 26)
        signal[day] = CalcEMA(macd, day, 9)

        if macd[day] > signal[day]:
            # buy shares
            capital, shares = buy_shares(capital, prices[day], shares)
            #capitalSell.append(capital)
        elif macd[day] < signal[day]:
            # sell shares
            if (shares > 0):
                capital, shares = sell_shares(capital, prices[day], shares)
                capitalSell.append(capital)



        capitalTab[day] = capital
        # sell all remaining shares
    capital, shares = sell_shares(capital, prices[-1], shares)
    print(f"Final capital: {capital:.2f}")


    printGraph(prices, macd, signal, capitalSell)

if __name__ == '__main__':
    main()