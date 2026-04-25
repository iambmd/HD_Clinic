#!/usr/bin/env python
"""
Run this script to populate the HES Clinic database with sample data.
Usage:  python setup_sample_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hes_clinic.settings')
django.setup()

from clinic.models import Service, Doctor, Article
from django.contrib.auth import get_user_model

User = get_user_model()

print("🏥  Setting up HES Clinic sample data...\n")

# ── SERVICES ──────────────────────────────────────────────
SERVICES = [
    # (title_en, title_vi, desc_en, desc_vi, icon, category)
    ('Otitis Media', 'Viêm Tai Giữa',
     'Diagnosis and treatment of middle ear infections including acute, chronic, and recurring cases for all age groups.',
     'Chẩn đoán và điều trị viêm tai giữa cấp tính, mãn tính và tái phát cho mọi lứa tuổi.',
     'bi-ear', 'EAR'),
    ('Sudden Hearing Loss', 'Điếc Đột Ngột',
     'Urgent diagnosis and treatment for sudden sensorineural hearing loss using corticosteroid therapy and intratympanic injections.',
     'Chẩn đoán và điều trị khẩn cấp điếc đột ngột bằng liệu pháp corticosteroid và tiêm nội nhĩ.',
     'bi-volume-mute', 'EAR'),
    ('Tinnitus', 'Ù Tai',
     'Comprehensive assessment and management of persistent ringing, buzzing, or hissing sounds in the ears.',
     'Đánh giá và quản lý toàn diện tiếng ù, vo ve hoặc rít kéo dài trong tai.',
     'bi-soundwave', 'EAR'),
    ('Ear Wax Removal', 'Lấy Ráy Tai',
     'Safe and professional ear wax extraction using modern micro-suction and irrigation techniques.',
     'Lấy ráy tai an toàn và chuyên nghiệp bằng kỹ thuật hút vi mô và tưới rửa hiện đại.',
     'bi-tools', 'EAR'),
    ('Sinusitis', 'Viêm Xoang',
     'Treatment of acute and chronic sinusitis including nasal endoscopy, saline irrigation, and medical management.',
     'Điều trị viêm xoang cấp và mãn tính bao gồm nội soi mũi, tưới rửa nước muối và điều trị thuốc.',
     'bi-wind', 'NOSE'),
    ('Nasal Polyps', 'Polyp Mũi',
     'Diagnosis and medical or surgical removal of nasal polyps causing breathing difficulty and reduced smell.',
     'Chẩn đoán và loại bỏ polyp mũi bằng thuốc hoặc phẫu thuật khi gây khó thở và giảm khứu giác.',
     'bi-droplet', 'NOSE'),
    ('Allergic Rhinitis', 'Viêm Mũi Dị Ứng',
     'Expert management of seasonal and perennial allergic rhinitis including allergen testing and immunotherapy.',
     'Điều trị viêm mũi dị ứng theo mùa và quanh năm bao gồm xét nghiệm dị nguyên và liệu pháp miễn dịch.',
     'bi-flower1', 'NOSE'),
    ('Deviated Nasal Septum', 'Lệch Vách Ngăn Mũi',
     'Assessment and surgical correction of nasal septal deviation that affects breathing and causes recurrent infections.',
     'Đánh giá và phẫu thuật chỉnh hình lệch vách ngăn mũi ảnh hưởng đến hô hấp và gây nhiễm trùng tái phát.',
     'bi-arrows-expand', 'NOSE'),
    ('Pharyngitis', 'Viêm Họng',
     'Diagnosis and treatment of acute and chronic throat inflammation caused by viral, bacterial, or fungal infections.',
     'Chẩn đoán và điều trị viêm họng cấp và mãn tính do vi rút, vi khuẩn hoặc nấm gây ra.',
     'bi-mic', 'THROAT'),
    ('Laryngitis & Voice Disorders', 'Viêm Thanh Quản & Rối Loạn Giọng Nói',
     'Treatment of voice box inflammation including hoarseness, voice fatigue, and complete voice loss.',
     'Điều trị viêm thanh quản bao gồm khàn giọng, mệt giọng và mất tiếng hoàn toàn.',
     'bi-mic-mute', 'THROAT'),
    ('Tonsillitis', 'Viêm Amidan',
     'Diagnosis and management of tonsil and adenoid inflammation, including surgical options for recurrent cases.',
     'Chẩn đoán và điều trị viêm amidan và V.A., bao gồm phẫu thuật cho các trường hợp tái phát.',
     'bi-shield-plus', 'THROAT'),
    ('Acid Reflux (GERD/LPR)', 'Trào Ngược Dạ Dày – Thực Quản',
     'Diagnosis and treatment of ENT complications from gastroesophageal and laryngopharyngeal reflux.',
     'Chẩn đoán và điều trị các biến chứng Tai Mũi Họng do trào ngược dạ dày thực quản và hầu thanh quản.',
     'bi-activity', 'THROAT'),
]

created_s = 0
for s in SERVICES:
    obj, created = Service.objects.get_or_create(
        title_en=s[0],
        defaults=dict(title_vi=s[1], description_en=s[2], description_vi=s[3], icon=s[4], category=s[5])
    )
    if created:
        created_s += 1

print(f"  ✅  Services: {Service.objects.count()} total ({created_s} new)")

# ── DOCTORS ───────────────────────────────────────────────
DOCTORS = [
    ('Dr. Hong Son Bui (Bùi Hồng Sơn)',
     'MS in ENT – Head Physician & Founder',
     "Dr. Bui Hong Son is the founder and head physician of HES Clinic. Holding a Master's degree in Otolaryngology (Ear, Nose & Throat), he brings extensive clinical expertise and a genuine passion for patient care. He specialises in diagnosing and treating complex ENT conditions using evidence-based, patient-centred approaches.",
     "Bác sĩ Bùi Hồng Sơn là người sáng lập và bác sĩ trưởng của Phòng Khám HES. Với bằng Thạc sĩ Tai Mũi Họng, ông có nhiều năm kinh nghiệm lâm sàng và niềm đam mê thực sự với việc chăm sóc bệnh nhân. Ông chuyên chẩn đoán và điều trị các bệnh lý Tai Mũi Họng phức tạp bằng phương pháp dựa trên bằng chứng, lấy bệnh nhân làm trung tâm."),
]

created_d = 0
for d in DOCTORS:
    obj, created = Doctor.objects.get_or_create(
        name=d[0],
        defaults=dict(specialty=d[1], bio_en=d[2], bio_vi=d[3])
    )
    if created:
        created_d += 1

print(f"  ✅  Doctors:  {Doctor.objects.count()} total ({created_d} new)")

# ── ARTICLES ──────────────────────────────────────────────
ARTICLES = [
    ('5 Signs You Should See an ENT Specialist',
     '5 Dấu Hiệu Cần Đến Gặp Bác Sĩ Tai Mũi Họng',
     """Many people ignore symptoms that are actually warning signs of an ENT condition that needs professional attention. Here are five signs you should book an appointment:

1. Persistent Ear Pain or Pressure – Ear pain lasting more than a few days, especially with fever or discharge, may indicate an infection or other condition requiring treatment.

2. Chronic Nasal Congestion – If your nose has been blocked for more than 3 weeks, you may have sinusitis, nasal polyps, or a structural issue like a deviated septum.

3. Hoarseness or Voice Changes – A voice that is raspy, weak, or has changed significantly for more than 2 weeks should be evaluated to rule out vocal cord issues or other throat conditions.

4. Difficulty Swallowing – Painful or difficult swallowing can be caused by tonsillitis, throat infections, acid reflux, or in rare cases, more serious conditions.

5. Recurring Sore Throats – If you are getting sore throats more than 4–5 times a year, it may be time to discuss whether your tonsils need attention.

At HES Clinic, our specialists can evaluate all of these symptoms and create an effective, personalised treatment plan for you. Don't wait — early diagnosis leads to better outcomes.""",
     """Nhiều người bỏ qua các triệu chứng thực ra là dấu hiệu cảnh báo của bệnh lý Tai Mũi Họng cần được chăm sóc chuyên nghiệp. Dưới đây là năm dấu hiệu bạn nên đặt lịch hẹn khám:

1. Đau tai hoặc áp lực kéo dài – Đau tai kéo dài hơn vài ngày, đặc biệt kèm theo sốt hoặc chảy dịch, có thể chỉ ra nhiễm trùng hoặc tình trạng khác cần điều trị.

2. Nghẹt mũi mãn tính – Nếu mũi bạn bị nghẹt hơn 3 tuần, bạn có thể bị viêm xoang, polyp mũi hoặc vấn đề cấu trúc như lệch vách ngăn mũi.

3. Khàn giọng hoặc thay đổi giọng nói – Giọng nói khàn khàn, yếu ớt hoặc thay đổi đáng kể hơn 2 tuần cần được đánh giá để loại trừ các vấn đề về dây thanh âm.

4. Khó nuốt – Nuốt đau hoặc khó có thể do viêm amidan, nhiễm trùng họng, trào ngược axit hoặc trong một số ít trường hợp là các tình trạng nghiêm trọng hơn.

5. Đau họng tái phát – Nếu bạn bị đau họng hơn 4–5 lần mỗi năm, đã đến lúc thảo luận về việc liệu amidan của bạn có cần can thiệp không.

Tại Phòng Khám HES, các chuyên gia của chúng tôi có thể đánh giá tất cả các triệu chứng này và xây dựng kế hoạch điều trị hiệu quả, cá nhân hóa cho bạn.""",
     '5-signs-you-should-see-ent-specialist'),

    ('How to Prevent Sinusitis During Season Changes',
     'Cách Phòng Ngừa Viêm Xoang Khi Chuyển Mùa',
     """Sinusitis is one of the most common reasons people visit an ENT clinic, particularly during Vietnam's seasonal transitions when temperature and humidity shift dramatically. Here's how to reduce your risk:

Stay Hydrated – Drinking plenty of water keeps your nasal passages moist and helps flush out pathogens. Aim for at least 2 litres per day.

Use Saline Nasal Rinses – A simple saline rinse once or twice daily washes away allergens, pollutants, and virus particles before they can trigger inflammation.

Manage Allergies Early – If you have allergic rhinitis, treating it proactively with antihistamines or nasal steroid sprays (under medical guidance) prevents the swelling that can lead to sinusitis.

Keep Indoor Humidity in Check – Use a humidifier when indoor air is dry, but avoid excessive humidity which can encourage mould growth. The sweet spot is 40–50%.

Boost Your Immune System – Adequate sleep, a balanced diet rich in vitamins C and D, and regular moderate exercise all support immune function and reduce infection risk.

Avoid Sudden Temperature Changes – Moving rapidly between hot outdoor air and cold air-conditioned spaces stresses the nasal mucosa. Carry a light jacket and allow your body to acclimatise gradually.

If you develop sinus symptoms, visit HES Clinic early — prompt treatment prevents acute sinusitis from progressing to a chronic condition.""",
     """Viêm xoang là một trong những lý do phổ biến nhất khiến mọi người đến phòng khám Tai Mũi Họng, đặc biệt trong các đợt chuyển mùa ở Việt Nam khi nhiệt độ và độ ẩm thay đổi đột ngột.

Uống đủ nước – Uống nhiều nước giúp giữ ẩm đường mũi và hỗ trợ đào thải mầm bệnh. Hãy uống ít nhất 2 lít mỗi ngày.

Dùng nước muối sinh lý rửa mũi – Rửa mũi bằng nước muối sinh lý một đến hai lần mỗi ngày giúp loại bỏ dị nguyên, chất ô nhiễm và các hạt vi rút trước khi chúng gây viêm.

Kiểm soát dị ứng sớm – Nếu bạn bị viêm mũi dị ứng, điều trị dự phòng bằng thuốc kháng histamine hoặc xịt steroid mũi giúp ngăn phù nề dẫn đến viêm xoang.

Duy trì độ ẩm trong nhà – Sử dụng máy tạo ẩm khi không khí trong nhà khô, nhưng tránh độ ẩm quá cao có thể tạo điều kiện cho nấm mốc phát triển.

Tăng cường hệ miễn dịch – Ngủ đủ giấc, chế độ ăn cân bằng giàu vitamin C và D, và tập thể dục điều độ đều hỗ trợ chức năng miễn dịch.

Nếu bạn có triệu chứng xoang, hãy đến Phòng Khám HES sớm — điều trị kịp thời ngăn viêm xoang cấp tính tiến triển thành mãn tính.""",
     'prevent-sinusitis-during-season-changes'),

    ('Understanding Hearing Loss: Types, Causes & Treatments',
     'Hiểu Về Mất Thính Lực: Các Loại, Nguyên Nhân và Điều Trị',
     """Hearing loss affects people of all ages and can have a profound impact on quality of life. Understanding the different types can help you seek the right care sooner.

Types of Hearing Loss

Conductive Hearing Loss occurs when sound cannot pass efficiently through the outer or middle ear. Common causes include ear wax blockage, fluid in the middle ear, perforated eardrums, or otosclerosis. This type is often treatable with medication or surgery.

Sensorineural Hearing Loss (SNHL) results from damage to the inner ear (cochlea) or the auditory nerve. Causes include ageing (presbycusis), prolonged noise exposure, viral infections, or sudden hearing loss. Treatment may include hearing aids or cochlear implants.

Mixed Hearing Loss is a combination of both conductive and sensorineural components and requires a tailored treatment approach.

Warning Signs
- Frequently asking others to repeat themselves
- Difficulty understanding speech in noisy environments
- Turning up the TV or radio louder than others prefer
- Ringing in the ears (tinnitus)
- Sudden change in hearing in one or both ears

When to Seek Help
Any sudden change in hearing is a medical emergency and should be evaluated within 24–72 hours for the best chance of recovery. Gradual hearing changes should be assessed as soon as noticed.

At HES Clinic, we offer comprehensive audiological testing and personalised treatment plans. Book your hearing assessment today.""",
     """Mất thính lực ảnh hưởng đến mọi lứa tuổi và có thể tác động sâu sắc đến chất lượng cuộc sống. Hiểu các loại khác nhau có thể giúp bạn tìm kiếm sự chăm sóc phù hợp sớm hơn.

Các loại mất thính lực

Mất thính lực dẫn truyền xảy ra khi âm thanh không thể truyền hiệu quả qua tai ngoài hoặc tai giữa. Nguyên nhân thường gặp bao gồm tắc ráy tai, dịch trong tai giữa, thủng màng nhĩ hoặc xốp xơ tai. Loại này thường có thể điều trị bằng thuốc hoặc phẫu thuật.

Mất thính lực thần kinh cảm giác (SNHL) do tổn thương tai trong (ốc tai) hoặc dây thần kinh thính giác. Nguyên nhân bao gồm lão hóa, tiếp xúc tiếng ồn kéo dài, nhiễm trùng virus hoặc điếc đột ngột. Điều trị có thể bao gồm máy trợ thính hoặc cấy ghép ốc tai điện tử.

Mất thính lực hỗn hợp là sự kết hợp của cả hai loại và cần phương pháp điều trị phù hợp riêng.

Dấu hiệu cảnh báo cần chú ý bao gồm: thường xuyên yêu cầu người khác nhắc lại, khó hiểu lời nói trong môi trường ồn ào, và ù tai kèm theo thay đổi thính lực đột ngột.

Tại Phòng Khám HES, chúng tôi cung cấp kiểm tra thính học toàn diện và kế hoạch điều trị cá nhân hóa.""",
     'understanding-hearing-loss-types-causes-treatments'),
]

created_a = 0
for a in ARTICLES:
    obj, created = Article.objects.get_or_create(
        slug=a[4],
        defaults=dict(title_en=a[0], title_vi=a[1], content_en=a[2], content_vi=a[3])
    )
    if created:
        created_a += 1

print(f"  ✅  Articles:  {Article.objects.count()} total ({created_a} new)")

# ── SUPERUSER ─────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@hesclinic.com', 'admin1234')
    print("  ✅  Admin user created  →  username: admin  |  password: admin1234")
else:
    print("  ✅  Admin user already exists")

print("\n✅  Setup complete! Run:  python manage.py runserver")
print("   Admin panel:  http://127.0.0.1:8000/admin/")
print("   Website:      http://127.0.0.1:8000/")
