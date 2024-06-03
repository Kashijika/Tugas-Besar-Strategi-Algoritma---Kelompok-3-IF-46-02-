import streamlit as st
import pandas as pd
import time

def knapsack_brute_force(weights, profits, max_weight):
    n = len(weights)
    max_profit = 0
    best_combination = []
    steps = []

    def evaluate_subset(subset):
        total_weight = 0
        total_profit = 0
        for i in range(n):
            if subset[i]:
                total_weight += weights[i]
                total_profit += profits[i]
        return total_weight, total_profit

    for i in range(1 << n):
        subset = [(i >> j) & 1 for j in range(n)]
        total_weight, total_profit = evaluate_subset(subset)
        steps.append((subset, total_weight, total_profit))
        if total_weight <= max_weight and total_profit > max_profit:
            max_profit = total_profit
            best_combination = subset

    return max_profit, best_combination, steps

def knapsack_greedy(weights, profits, max_weight, criterion):
    n = len(weights)
    indices = list(range(n))
    steps = []

    if criterion == "weight":
        indices.sort(key=lambda i: weights[i])
    elif criterion == "profit":
        indices.sort(key=lambda i: profits[i], reverse=True)
    elif criterion == "density":
        indices.sort(key=lambda i: profits[i] / weights[i], reverse=True)

    total_weight = 0
    total_profit = 0
    selected = [0] * n

    for i in indices:
        if total_weight + weights[i] <= max_weight:
            total_weight += weights[i]
            total_profit += profits[i]
            selected[i] = 1
        profit_weight_ratio = profits[i] / weights[i]
        steps.append((i, total_weight, total_profit, selected.copy(), profit_weight_ratio))

    return total_profit, selected, steps

def main():
    # Pembukaan Web
    st.title('Astra Militarum: Conquering Europe!')
    st.header('Prepare your troops, commander!')

    if 'algorithm' not in st.session_state:
        st.session_state.algorithm = None
    if 'criterion' not in st.session_state:
        st.session_state.criterion = None

    num_divisions = st.number_input("Masukkan jumlah divisi:", min_value=1, step=1)
    max_weight = st.number_input("Masukkan jumlah maksimum prajurit:", min_value=1, step=1)
    
    weights = []
    profits = []

    for i in range(num_divisions):
        weight = st.number_input(f"Masukkan jumlah prajurit untuk divisi {i+1}:", min_value=1, step=1)
        profit = st.number_input(f"Masukkan rating pengalaman untuk divisi {i+1} (1-10):", min_value=1, max_value=10, step=1)
        weights.append(weight)
        profits.append(profit)

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Brute Force'):
            st.session_state.algorithm = "Brute Force"
            st.session_state.criterion = None
    with col2:
        if st.button('Greedy'):
            st.session_state.algorithm = "Greedy"
            st.session_state.criterion = None

    if st.session_state.algorithm == "Greedy":
        st.subheader("Pilih Kriteria Greedy:")
        col3, col4, col5 = st.columns(3)
        with col3:
            if st.button('By Weight'):
                st.session_state.criterion = 'weight'
        with col4:
            if st.button('By Profit'):
                st.session_state.criterion = 'profit'
        with col5:
            if st.button('By Density'):
                st.session_state.criterion = 'density'
    
    if st.session_state.algorithm and (st.session_state.algorithm == "Brute Force" or st.session_state.criterion):
        if st.button('Hitung Solusi'):
            if st.session_state.algorithm == "Brute Force":
                # Jalankan metode brute force
                start_time = time.time()
                max_profit, best_combination, steps = knapsack_brute_force(weights, profits, max_weight)
                execution_time = time.time() - start_time

                # Output hasil brute force
                st.subheader("Detail Unit yang Sudah Terdaftar:")
                for i in range(num_divisions):
                    st.subheader(f"No. Divisi {i+1}:")
                    st.write(f"Jumlah Prajurit: {weights[i]}")
                    st.write(f"Rating Pengalaman: {profits[i]}")
                    st.write("")
                st.write("Berdasarkan data-data yang telah dimasukkan, berikut data dalam bentuk tabel knapsack:")
                st.write("")

                # Tabel Knapsack
                st.subheader("Tabel Knapsack:")
                df = pd.DataFrame({
                    'No. Divisi': list(range(1, num_divisions + 1)),
                    'Jumlah Pasukan': weights,
                    'Rating Pengalaman': profits
                })
                st.write(df)

                # Definisi Algoritma Brute Force
                st.subheader("Definisi Algoritma Brute Force:")
                st.write("""
                    Algoritma Brute Force merupakan algoritma yang mengevaluasi setiap kemungkinan kombinasi divisi untuk 
                    menentukan kombinasi dengan total keuntungan maksimum (Max Profit) tanpa melebihi jumlah prajurit maksimum (Max Weight)

                    Dalam konteks kasus ini, Jumlah Pasukan merupakan Weight dan Jumlah Rating Pengalaman merupakan Profit.
                """)

                # Langkah-langkah Brute Force
                st.subheader("Langkah-langkah Brute Force:")
                steps_df = pd.DataFrame([{'Kombinasi': s[0], 'Total Berat': s[1], 'Total Keuntungan': s[2]} for s in steps])
                st.write(steps_df)

                #Summary Hasil Brute Force
                st.subheader("Summary Hasil:")
                st.write(f"Berdasarkan hasil analisis dari Tabel Knapsack Kombinasi yang telah dibuat, dapat dilihat bahwa Divisi yang terpilih adalah: ")
                for i in range(num_divisions):
                        if best_combination[i]:
                            st.subheader(f"Divisi {i+1}")
                            st.write(f"Jumlah Pasukan: {weights[i]}")
                            st.write(f"Rating Pengalaman: {profits[i]}")
                            st.write("")
                st.write(f"Pengalaman maksimum: {max_profit}")
                st.write("")
                st.write(f"""
                    Divisi yang tidak masuk dalam kombinasi, tidak terpilih dikarenakan dalam metode Brute Force, divisi tersebut
                    memiliki nilai weight yang besar sehingga dan akan melewati batas maksimum berat (Max Weight) jika dipilih.
                """)
            
                st.subheader(f"Waktu eksekusi: {execution_time:.6f} detik")

            elif st.session_state.algorithm == "Greedy" and st.session_state.criterion:
                # Jalankan metode greedy berdasarkan kriteria yang dipilih
                start_time = time.time()
                max_profit, best_combination, steps = knapsack_greedy(weights, profits, max_weight, st.session_state.criterion)
                execution_time = time.time() - start_time

                # Output hasil greedy
                st.subheader(f"Detail Unit yang Sudah Terdaftar:")
                for i in range(num_divisions):
                    st.subheader(f"No. Divisi {i+1}:")
                    st.write(f"Jumlah Prajurit: {weights[i]}")
                    st.write(f"Rating Pengalaman: {profits[i]}")
                    st.write("")
                st.write("Berdasarkan data-data yang telah dimasukkan, berikut data dalam bentuk tabel knapsack:")
                st.write("")

                # Tabel Knapsack
                st.subheader("Tabel Knapsack:")
                df = pd.DataFrame({
                    'No. Divisi': list(range(1, num_divisions + 1)),
                    'Jumlah Pasukan': weights,
                    'Rating Pengalaman': profits
                })
                st.write(df)

                # Definisi Algoritma Greedy
                if st.session_state.criterion == "weight":
                    st.subheader("Definisi Algoritma Greedy (Weight):")
                    st.write("""
                        Algoritma Greedy by Weight merupakan algoritma yang memilih item satu per satu dari berat (Weight) yang paling ringan hingga 
                        terberat, dan memasukkannya ke dalam kombinasi selama total berat (Total Weight) tidak melebihi jumlah berat maksimum. (Max Weight)

                        Dalam konteks kasus ini, Jumlah Pasukan merupakan Weight dan Jumlah Rating Pengalaman merupakan Profit.
                    """)

                    # Langkah-langkah Greedy (Weight)
                    st.subheader(f"Langkah-langkah Greedy (Weight):")
                    steps_df = pd.DataFrame([{
                        'No. Divisi': s[0] + 1, 
                        'Total Pasukan': s[1], 
                        'Total Pengalaman': s[2], 
                        'Kombinasi Divisi': s[3]} for s in steps])
                    st.write(steps_df)

                    #Summary hasil Greedy by Weight
                    st.subheader("Summary Hasil:")
                    st.write(f"Berdasarkan hasil analisis dari Tabel Knapsack Kombinasi yang telah dibuat, dapat dilihat bahwa Divisi yang terpilih adalah: ")
                    for i in range(num_divisions):
                        if best_combination[i]:
                            st.subheader(f"Divisi {i+1}")
                            st.write(f"Jumlah Pasukan: {weights[i]}")
                            st.write(f"Rating Pengalaman: {profits[i]}")
                            st.write("")
                    st.write(f"Pengalaman maksimum: {max_profit}")
                    st.write("")
                    st.write(f"""
                        Divisi yang tidak masuk dalam kombinasi, tidak terpilih dikarenakan dalam metode Greedy by Weight, divisi tersebut
                        memiliki nilai Weight yang besar sehingga terurut di belakang dalam urutan pemilihan dan akan melewati batas maksimum berat (Max Weight)
                        jika dipilih.
                    """)

                elif st.session_state.criterion == "profit":
                    st.subheader("Definisi Algoritma Greedy (Profit):")
                    st.write("""
                        Algoritma Greedy by Profit merupakan algoritma yang memilih item satu per satu dari yang memiliki keuntungan (Profit) terbesar 
                        hingga terkecil, dan memasukkannya ke dalam kombinasi selama total berat (Total Weight) tidak melebihi jumlah berat maksimum. (Max Weight)

                        Dalam konteks kasus ini, Jumlah Pasukan merupakan Weight dan Jumlah Rating Pengalaman merupakan Profit.
                    """)

                    # Langkah-langkah Greedy (Profit)
                    st.subheader(f"Langkah-langkah Greedy (Profit):")
                    steps_df = pd.DataFrame([{
                        'No. Divisi': s[0] + 1, 
                        'Total Pasukan': s[1], 
                        'Total Pengalaman': s[2], 
                        'Kombinasi Divisi': s[3]} for s in steps])
                    st.write(steps_df)

                    #Summary hasil Greedy by Profit
                    st.subheader("Summary Hasil:")
                    st.write(f"Berdasarkan hasil analisis dari Tabel Knapsack Kombinasi yang telah dibuat, dapat dilihat bahwa Divisi yang terpilih adalah: ")
                    for i in range(num_divisions):
                        if best_combination[i]:
                            st.subheader(f"Divisi {i+1}")
                            st.write(f"Jumlah Pasukan: {weights[i]}")
                            st.write(f"Rating Pengalaman: {profits[i]}")
                            st.write("")
                    st.write(f"Pengalaman maksimum: {max_profit}")
                    st.write("")
                    st.write(f"""
                        Divisi yang tidak masuk dalam kombinasi, tidak terpilih dikarenakan dalam metode Greedy by Profit, divisi tersebut
                        memiliki nilai Profit yang kecil sehingga terurut di belakang dalam urutan pemilihan dan akan melewati batas maksimum berat (Max Weight)
                        jika dipilih.
                    """)

                elif st.session_state.criterion == "density":
                    st.subheader("Definisi Algoritma Greedy (Density):")
                    st.write("""
                        Algoritma Greedy by Density merupkana algoritma yang memilih item satu per satu dari yang memiliki rasio keuntungan (Profit) per berat (Weight)
                        terbesar hingga terkecil, dan memasukkannya ke dalam kombinasi selama total berat (Total Weight) tidak melebihi jumlah berat maksimum. (Max Weight)

                        Dalam konteks kasus ini, Jumlah Pasukan merupakan Weight dan Jumlah Rating Pengalaman merupakan Profit.
                    """)

                    # Langkah-langkah Greedy (Density)
                    steps_df = pd.DataFrame([{
                        'No. Divisi': s[0] + 1, 
                        'Total Pasukan': s[1], 
                        'Total Pengalaman': s[2],
                        'Kombinasi Divisi': s[3]} for s in steps])
                    st.write(steps_df)

                    #Summary hasil Greedy by Density
                    st.subheader("Summary Hasil:")
                    st.write(f"Berdasarkan hasil analisis dari Tabel Knapsack Kombinasi yang telah dibuat, dapat dilihat bahwa Divisi yang terpilih adalah: ")
                    for i in range(num_divisions):
                        if best_combination[i]:
                            st.subheader(f"Divisi {i+1}")
                            st.write(f"Jumlah Pasukan: {weights[i]}")
                            st.write(f"Rating Pengalaman: {profits[i]}")
                            st.write("")
                    st.write(f"Pengalaman maksimum: {max_profit}")
                    st.write("")
                    st.write(f"""
                        Divisi yang tidak masuk dalam kombinasi, tidak terpilih dikarenakan dalam metode Greedy by Density, divisi tersebut
                        memiliki nilai Density yang kecil sehingga terurut di belakang dalam urutan pemilihan dan akan melewati batas maksimum berat (Max Weight)
                        jika dipilih.
                    """)


                
                st.subheader(f"Waktu eksekusi: {execution_time:.6f} detik")

if __name__ == "__main__":
    main()