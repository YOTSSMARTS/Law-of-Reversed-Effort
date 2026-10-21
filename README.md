# NEWS CENTER — รวมข่าวในหน้าเดียว

เว็บไซต์รวมพาดหัวข่าวจาก RSS สาธารณะ พร้อมค้นหาและกรองหมวดข่าว โดยลิงก์ข่าวจะเปิดไปยังต้นทาง

## หมวดข่าว
- ข่าวไทย
- ข่าวโลก
- เศรษฐกิจและการเงิน
- เทคโนโลยีและ AI
- ธุรกิจ

## เปิดเว็บไซต์ด้วย GitHub Pages
1. เข้า **Settings → Pages** ของ repository นี้
2. ใน **Build and deployment** เลือก **Deploy from a branch**
3. เลือก branch `main` และ folder `/(root)` แล้วกด **Save**
4. รอ GitHub เผยแพร่เว็บไซต์ จากนั้น URL จะปรากฏในหน้า Pages (โดยทั่วไปเป็น `https://yotssmarts.github.io/Law-of-Reversed-Effort/`)

## เปิดการอัปเดตข่าวอัตโนมัติ
1. เข้า **Actions** และอนุญาต workflows หาก GitHub ขอให้เปิดใช้งาน
2. เข้า **Settings → Actions → General → Workflow permissions** แล้วเลือก **Read and write permissions** เพื่อให้ workflow บันทึกไฟล์ `data/news.json` ได้
3. ในแท็บ **Actions** เลือก workflow **Refresh news feeds** แล้วกด **Run workflow** เพื่อทดสอบครั้งแรก

Workflow จะพยายามดึง Google News RSS ทุก 5 นาทีและอัปเดต `data/news.json` หากมีข้อมูลเปลี่ยนแปลง ทั้งนี้ GitHub อาจเลื่อนเวลารันตามภาระระบบหรือข้อจำกัดของบัญชี และฟีดข่าวบางรายการอาจไม่พร้อมใช้งานทุกครั้ง

## ไฟล์หลัก
- `index.html` — หน้าเว็บค้นหาและกรองข่าว
- `scripts/fetch_news.py` — ตัวรวบรวม RSS
- `.github/workflows/refresh-news.yml` — ตารางรันอัตโนมัติ
- `data/news.json` — ข้อมูลข่าวล่าสุดที่หน้าเว็บอ่าน

## ข้อจำกัด
การรวม RSS ไม่สามารถรับประกันว่าจะได้ข่าวทุกชิ้นหรือข้อมูลทันทีแบบวินาทีต่อวินาที รายการข่าวแสดงพาดหัว แหล่งข่าว เวลาเผยแพร่เมื่อมี และลิงก์ต้นฉบับ ไม่ได้คัดลอกเนื้อหาบทความเต็ม
