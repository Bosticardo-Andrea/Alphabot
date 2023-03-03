class Hash:
    def __init__(self):
        self.stringa = ""
        self.primiOtto = ["01101010000010011110011001100111","10111011011001111010111010000101","00111100011011101111001101110010","10100101010011111111010100111010",
            "01010001000011100101001001111111","10011011000001010110100010001100","00011111100000111101100110101011","01011011111000001100110100011001"]
        self.w = ["01000010100010100010111110011000",
"01110001001101110100010010010001",
"10110101110000001111101111001111",
"11101001101101011101101110100101",
"00111001010101101100001001011011",
"01011001111100010001000111110001",
"10010010001111111000001010100100",
"10101011000111000101111011010101",
"11011000000001111010101010011000",
"00010010100000110101101100000001",
"00100100001100011000010110111110",
"01010101000011000111110111000011",
"01110010101111100101110101110100",
"10000000110111101011000111111110",
"10011011110111000000011010100111",
"11000001100110111111000101110100",
"11100100100110110110100111000001",
"11101111101111100100011110000110",
"00001111110000011001110111000110",
"00100100000011001010000111001100",
"00101101111010010010110001101111",
"01001010011101001000010010101010",
"01011100101100001010100111011100",
"01110110111110011000100011011010",
"10011000001111100101000101010010",
"10101000001100011100011001101101",
"10110000000000110010011111001000",
"10111111010110010111111111000111",
"11000110111000000000101111110011",
"11010101101001111001000101000111",
"00000110110010100110001101010001",
"00010100001010010010100101100111",
"00100111101101110000101010000101",
"00101110000110110010000100111000",
"01001101001011000110110111111100",
"01010011001110000000110100010011",
"01100101000010100111001101010100",
"01110110011010100000101010111011",
"10000001110000101100100100101110",
"10010010011100100010110010000101",
"10100010101111111110100010100001",
"10101000000110100110011001001011",
"11000010010010111000101101110000",
"11000111011011000101000110100011",
"11010001100100101110100000011001",
"11010110100110010000011000100100",
"11110100000011100011010110000101",
"00010000011010101010000001110000",
"00011001101001001100000100010110",
"00011110001101110110110000001000",
"00100111010010000111011101001100",
"00110100101100001011110010110101",
"00111001000111000000110010110011",
"01001110110110001010101001001010",
"01011011100111001100101001001111",
"01101000001011100110111111110011",
"01110100100011111000001011101110",
"01111000101001010110001101101111",
"10000100110010000111100000010100",
"10001100110001110000001000001000",
"10010000101111101111111111111010",
"10100100010100000110110011101011",
"10111110111110011010001111110111",
"11000110011100010111100011110010"]
    def dividiInBit(self,nBit):
        stringaInBit,finale = "".join(self.dec2bin(ord(cella), 8) for cella in self.stringa),[]
        stringaInBit += "1" +"0"*(503 - len(stringaInBit)) + self.dec2bin(len(stringaInBit), 8)
        for k in range(0,len(stringaInBit),nBit):
            finale.append(stringaInBit[k:k+nBit])
        return finale
    def shift(self,stringa,n):
        for k in range(n):
            stringa = stringa[-1] + stringa[:-1] 
        return stringa
    def bin2dec(self,stringa):
        dec = 0
        for k,carattere in enumerate(stringa[::-1]): 
            if carattere == "1": dec += 2 ** k
        return dec
    def NOT(self,pezzo):
        ris = ""
        for cella in pezzo:
            if cella == "0": ris+= "1"
            else: ris+= "0"
        return ris
    def dec2bin(self,numero,nbit):
        numeroBin = bin(numero)[2:]
        return "0" * (nbit-len(numeroBin))+numeroBin
    def creaTutteChiavi(self):
        for k in range(48): self.stringa.append(self.dec2bin(self.bin2dec(self.stringa[k]) + self.XOR_SHIFT(self.stringa[k+1],7,18,3) + self.bin2dec(self.stringa[k+9]) + self.XOR_SHIFT(self.stringa[k+14],17,19,10),32))
    def XOR(self,pezzo1,pezzo2): return self.dec2bin(self.bin2dec(pezzo1) ^ self.bin2dec(pezzo2),32)[-32:]
    def XOR_SHIFT(self, pezzo,shift1,shift2,shift3): return  self.bin2dec(self.XOR(self.XOR(self.shift(pezzo,shift1),self.shift(pezzo,shift2)),self.shift(pezzo,shift3))[-32:])
    def AND(self,pezzo,pezzo2): return  self.dec2bin((self.bin2dec(pezzo) & self.bin2dec(pezzo2)),32)[-32:]
    def OR(self,pezzo,pezzo2): return self.dec2bin((self.bin2dec(pezzo) | self.bin2dec(pezzo2)),32)[-32:]
    def OR_ESA(self, pezzo1,pezzo2): return hex(self.bin2dec(self.dec2bin((self.bin2dec(pezzo1) + self.bin2dec(pezzo2)),32)[-32:]))[2:]
    def creaDigest(self,stringa):
        self.stringa = stringa
        self.stringa = self.dividiInBit(32)
        self.creaTutteChiavi()
        a,b,c,d,e,f,g,h = self.primiOtto[0],self.primiOtto[1],self.primiOtto[2],self.primiOtto[3],self.primiOtto[4],self.primiOtto[5],self.primiOtto[6],self.primiOtto[7]
        for k in range(64):
            temp1 = self.bin2dec(h) + self.XOR_SHIFT(e,6,11,25) + self.bin2dec(self.XOR(self.AND(e,f) ,self.AND(self.NOT(e),g))) + self.bin2dec(self.stringa[k]) + self.bin2dec(self.w[k])
            temp2 = (self.XOR_SHIFT(a,2,13,22) + self.bin2dec(self.XOR(self.XOR(self.AND(a,b),self.AND(a,c)),self.AND(b,c))))
            h = g
            g = f
            f = e  
            e = self.dec2bin(self.bin2dec(d) + temp1,32)[-32:]
            d = c
            c = b
            b = a
            a = self.dec2bin(temp1 + temp2,32)[-32:]
        return self.OR_ESA(a,self.primiOtto[0]) + self.OR_ESA(b,self.primiOtto[1]) + self.OR_ESA(c,self.primiOtto[2]) + self.OR_ESA(d,self.primiOtto[3]) + self.OR_ESA(e,self.primiOtto[4]) + self.OR_ESA(f,self.primiOtto[5]) + self.OR_ESA(g,self.primiOtto[6]) + self.OR_ESA(h,self.primiOtto[7])