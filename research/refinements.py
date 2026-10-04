from editorial import PROFILES as P
def change(name, **kw):P[name].update(kw)
change('Chimera',steps=[
 ('Normal Summon Mirror Swordknight; Tribute nó để gọi Big-Winged Berfomet từ Deck.', ['Mirror Swordknight','Big-Winged Berfomet']),
 ('Berfomet tìm Gazelle và Chimera Fusion; Fusion Berfomet trên sân với Gazelle trên tay để gọi Chimera the King of Phantom Beasts.', ['Big-Winged Berfomet','Gazelle the King of Mythical Claws','Chimera Fusion','Chimera the King of Phantom Beasts']),
 ('Gazelle làm Fusion Material tìm Cornfield Coatl; Berfomet làm nguyên liệu hồi Mirror Swordknight từ GY.', ['Gazelle the King of Mythical Claws','Cornfield Coatl','Big-Winged Berfomet','Mirror Swordknight'])],end=['Chimera the King of Phantom Beasts','Mirror Swordknight'],board='Chimera và Mirror Swordknight, Coatl trên tay; Swordknight có negate vì Chimera được tính tên Chimera the Flying Mythical Beast trên sân.',hand=0)
change('Dragonmaid',starters=['Chamber Dragonmaid','Dragonmaid Lorpar'],steps=[
 ('Normal Summon Chamber, tìm Dragonmaid Changeover.', ['Chamber Dragonmaid','Dragonmaid Changeover']),
 ('Dùng Changeover Fusion Chamber trên sân và Lorpar Level 8 trên tay để gọi Sheou.', ['Dragonmaid Changeover','Chamber Dragonmaid','Dragonmaid Lorpar','Dragonmaid Sheou']),
 ('Giữ Sheou để negate; khi negate resolve, trả Sheou về Extra Deck rồi gọi House từ Extra Deck.', ['Dragonmaid Sheou','House Dragonmaid'])],end=['Dragonmaid Sheou'],board='Sheou trước khi dùng negate; cần House trong Extra Deck để hoàn thành hiệu ứng đổi quái.')
change('Dragon Link',steps=[
 ('Quick Launch gọi Tracer; Link Tracer thành Striker Dragon để tìm Boot Sector Launch.', ['Quick Launch','Rokket Tracer','Striker Dragon','Boot Sector Launch']),
 ('Kích hoạt Boot Sector; Striker target chính nó và Tracer trong GY, phá Striker để lấy Tracer về tay.', ['Boot Sector Launch','Striker Dragon','Rokket Tracer']),
 ('Boot Sector gọi Tracer từ tay; Tracer phá Boot Sector để gọi Silverrokket từ Deck.', ['Boot Sector Launch','Rokket Tracer','Silverrokket Dragon']),
 ('Synchro Savage bằng Tracer Tuner Level 4 và Silverrokket Level 4; Savage equip Striker trong GY để nhận một Borrel Counter.', ['Rokket Tracer','Silverrokket Dragon','Borreload Savage Dragon','Striker Dragon'])],end=['Borreload Savage Dragon'],board='Savage equip Striker với một Borrel Counter; khóa DARK của Tracer vẫn áp dụng.')
change('Endymion',hand=1)
change('Ryzeal',hand=0)
change('Centur-Ion',starters=['Centur-Ion Primera'],hand=1,steps=[
 ('Normal Summon Primera, tìm Stand Up Centur-Ion! rồi kích hoạt Field Spell.', ['Centur-Ion Primera','Stand Up Centur-Ion!']),
 ('Stand Up discard một lá để đặt Trudea từ Deck vào Spell/Trap Zone; chưa dùng hiệu ứng Trudea tự đặt nên vẫn được gọi nó trong lượt này.', ['Stand Up Centur-Ion!','Centur-Ion Trudea']),
 ('Gọi Trudea từ Spell/Trap Zone và tăng Level lên 8; Synchro Auxila bằng Trudea Level 8 và Primera Tuner Level 4.', ['Centur-Ion Trudea','Centur-Ion Primera','Centur-Ion Auxila'])])
change('Voiceless Voice',tip='Negate của Skull Guardian cần điều khiển Lo trên sân. Lo trong GY chỉ hỗ trợ phần tăng ATK, không tự cho negate.')
change('Dinomorphia',steps=[
 ('Normal Summon Therizia, úp Frenzy từ Deck.', ['Dinomorphia Therizia','Dinomorphia Frenzy']),
 ('Trong Main Phase đối thủ, Frenzy trả nửa LP; Fusion Kentregina bằng Diplos trong Deck và Stealthbergia trong Extra Deck.', ['Dinomorphia Frenzy','Dinomorphia Kentregina','Dinomorphia Diplos','Dinomorphia Stealthbergia']),
 ('Kentregina trả nửa LP, banish Frenzy để sao chép hiệu ứng; dùng Therizia trong Deck và Kentregina thứ hai trong Extra Deck để Fusion Rexterm.', ['Dinomorphia Kentregina','Dinomorphia Frenzy','Dinomorphia Therizia','Dinomorphia Rexterm'])],end=['Dinomorphia Therizia','Dinomorphia Kentregina','Dinomorphia Rexterm'],board='Therizia, Kentregina đầu tiên và Rexterm; LP giảm hai lần, mỗi Frenzy dùng nguyên liệu từ Deck và Extra Deck.')
change('Purrely',starters=['Purrely Delicious Memory'],hand=1,turn='going-second',tip='Delicious Memory cần target một quái trên sân; Purrelyly dùng Memory trong GY để Xyz, Purrely dùng Memory trên tay.')
change('Runick',starters=['Runick Tip','Runick Freezing Curses'],hand=1,board='Hugin và Fountain; Freezing Curses cần một Effect Monster face-up đối thủ làm mục tiêu ở bước rút.')
change('Branded Predaplant',hand=2)
change('Ice Barrier',steps=[
 ('Normal Summon Revealer, discard một lá để gọi Mirror Mage Tuner Level 5 từ Deck.', ['Revealer of the Ice Barrier','Mirror Mage of the Ice Barrier']),
 ('Mirror Mage Tribute Revealer để gọi ba Token Level 1; tăng Level của Mirror Mage thêm 3 thành Level 8.', ['Mirror Mage of the Ice Barrier','Revealer of the Ice Barrier']),
 ('Synchro Lancea Level 10 bằng Mirror Mage Tuner Level 8 và hai Token Level 1; còn một Token trên sân.', ['Mirror Mage of the Ice Barrier','Lancea, Ancestral Dragon of the Ice Mountain'])],end=['Lancea, Ancestral Dragon of the Ice Mountain'],board='Lancea và một Token Ice Barrier; Lancea gọi Ice Barrier từ Deck khi đối thủ Special Summon theo giới hạn của nó.')
change('Memento',starters=['Mementotlan Tatsunootoshigo','Mementotlan Fusion'],hand=0,steps=[
 ('Khi không có quái face-up ngoài Memento, Special Summon Tatsunootoshigo từ tay.', ['Mementotlan Tatsunootoshigo']),
 ('Tatsunootoshigo phá chính nó Level 5, gửi Angwitch Level 4 và Goblin Level 1 từ Deck vào GY.', ['Mementotlan Tatsunootoshigo','Mementotlan Angwitch','Mementotlan Goblin']),
 ('Dùng Mementotlan Fusion; vì quái của bạn đã bị phá bởi hiệu ứng, xào Tatsunootoshigo và Angwitch từ GY vào Deck để Fusion Twin Dragon.', ['Mementotlan Fusion','Mementotlan Tatsunootoshigo','Mementotlan Angwitch','Mementotlan Twin Dragon'])],board='Twin Dragon và Goblin trong GY; search của Twin Dragon cần phá thêm một Memento trên tay/sân.',tip='Shleepy tự gọi chỉ trong lượt quái của bạn đã bị phá bởi hiệu ứng; bản thân nó không tự phá Angwitch để gọi.')
change('Crystron',steps=[
 ('Discard một Crystron khác Sulfefnir để gọi Sulfefnir từ tay hoặc GY, rồi phá chính Sulfefnir.', ['Crystron Sulfefnir']),
 ('Sulfefnir bị phá gọi Smiger từ Deck ở Defense.', ['Crystron Sulfefnir','Crystron Smiger']),
 ('Giữ Smiger hoặc phá nó để gọi Citree Tuner từ Deck. Nếu chọn Citree, cần thêm non-Tuner đủ tổng Level để có Machine Synchro trong build.', ['Crystron Smiger','Crystron Citree'])],board='Smiger, hoặc Citree với Smiger trong GY; cặp Level 2+3 chưa đủ Level cho Machine Synchro của mẫu này.')
change('Radiant Typhoon',starters=['Radiant Typhoon Eldam'],hand=0,steps=[
 ('Normal Summon Eldam, tìm Swen.', ['Radiant Typhoon Eldam','Radiant Typhoon Swen']),
 ('Nếu đối thủ không có Spell/Trap hoặc MST đã ở GY, Special Summon Swen từ tay; nếu chưa thỏa điều kiện thì giữ Swen.', ['Radiant Typhoon Swen','Mystical Space Typhoon']),
 ('Swen khi được triệu hồi tìm Radiant Typhoon Chant; giữ Quick-Play cho lượt đối thủ hoặc nhánh tiếp theo.', ['Radiant Typhoon Swen','Radiant Typhoon Chant'])],end=['Radiant Typhoon Eldam','Radiant Typhoon Swen'],board='Eldam và Swen khi điều kiện tự gọi hợp lệ, Chant trên tay; nếu không, chỉ có Eldam và Swen trên tay.')
change('Ancient Gear',starters=['Ancient Gear Statue'],hand=0,steps=[
 ('Normal Summon Statue, Tribute nó để gọi Dark Golem từ Deck, bỏ qua điều kiện triệu hồi.', ['Ancient Gear Statue','Ancient Gear Dark Golem']),
 ('Dark Golem tìm Ancient Gear Fusion và Fortress rồi discard Fortress. Dark Golem được tính tên Ancient Gear Golem trên sân.', ['Ancient Gear Dark Golem','Ancient Gear Fusion','Ancient Gear Fortress']),
 ('Fusion dùng Dark Golem trên sân và Wyvern, Statue, Tanker từ Deck để Fusion Chaos Ancient Gear Giant; được dùng Deck vì đã dùng Golem trên sân làm nguyên liệu.', ['Ancient Gear Fusion','Ancient Gear Dark Golem','Ancient Gear Wyvern','Ancient Gear Statue','Ancient Gear Tanker','Chaos Ancient Gear Giant'])],end=['Chaos Ancient Gear Giant'],board='Chaos Ancient Gear Giant đã Fusion bằng bốn Ancient Gear; sát thương còn phụ thuộc sân và tương tác đối thủ.',tip='Advance cấm úp bài cả lượt dùng nó. Dark Golem/Wyvern cấm úp sau search; chỉ dùng nhánh có đúng điều kiện.')
change('Gimmick Puppet',hand=0,steps=[
 ('Kích hoạt Mansion tìm Rouge Doll.', ['Mansion of the Dreadful Dolls','Gimmick Puppet Rouge Doll']),
 ('Rouge Doll trên tay reveal Fantasix Rank 8 để gọi chính nó và Bisque Doll Level 8 từ Deck.', ['Gimmick Puppet Rouge Doll','Gimmick Puppet Fantasix Machinix','Gimmick Puppet Bisque Doll']),
 ('Xyz Fantasix bằng hai Level 8, detach một nguyên liệu tìm Rank-Up-Magic Argent Chaos Force; resolve hồi tay Rouge nếu đã được detach.', ['Gimmick Puppet Fantasix Machinix','Rank-Up-Magic Argent Chaos Force','Gimmick Puppet Rouge Doll'])],end=['Gimmick Puppet Fantasix Machinix','Mansion of the Dreadful Dolls'],board='Mansion, Fantasix và Rank-Up-Magic trên tay; đã bị khóa Gimmick Puppet Extra Deck cả lượt.')
change('Six Samurai',starters=['Legendary Six Samurai - Kizan','Tactical Trainer of the Six Samurai'],steps=[
 ('Normal Summon Kizan Level 4.', ['Legendary Six Samurai - Kizan']),
 ('Special Summon Tactical Trainer Level 2 Tuner vì có Six Samurai khác tên.', ['Tactical Trainer of the Six Samurai']),
 ('Synchro Legendary Lord Six Samurai - Shi En Level 6; resolve search của Shi En và Trainer tìm Double Assault.', ['Legendary Lord Six Samurai - Shi En','Tactical Trainer of the Six Samurai','Six Strike - Double Assault'])],board='Shi En có negate hiệu ứng quái, Double Assault trên tay và một search Samurai/Shien; bonus Trainer giảm ATK đối thủ.')
change('Mitsurugi Orcust',starters=['Girsu, the Orcust Mekk-Knight'],hand=0,steps=[
 ('Normal Summon Girsu, gửi Harp Horror từ Deck vào GY.', ['Girsu, the Orcust Mekk-Knight','Orcust Harp Horror']),
 ('Banish Harp để gọi Knightmare từ Deck; không cần dùng Token cho line này.', ['Orcust Harp Horror','Orcust Knightmare']),
 ('Link Girsu và Knightmare, hai Effect Monster, thành Galatea; Galatea xào Harp banish về Deck để úp Babel, rồi kích hoạt Babel.', ['Girsu, the Orcust Mekk-Knight','Orcust Knightmare','Galatea, the Orcust Automaton','Orcustrated Babel'])],end=['Galatea, the Orcust Automaton','Orcustrated Babel'],board='Galatea và Babel, Knightmare trong GY; giữ hiệu ứng GY cho lượt đối thủ, đã khóa Special Summon DARK.')
change('Crystron',steps=[
 ('Discard một Crystron khác Sulfefnir để gọi Sulfefnir từ tay/GY, rồi phá chính Sulfefnir.', ['Crystron Sulfefnir']),
 ('Sulfefnir bị phá gọi Smiger từ Deck ở Defense; Smiger phá chính nó để gọi Citree Tuner Level 2.', ['Crystron Sulfefnir','Crystron Smiger','Crystron Citree']),
 ('Trong Main Phase hoặc Battle Phase đối thủ, Citree target Sulfefnir Level 5 trong GY, hồi nó và Synchro Dawn Dragster Level 7 bằng cả hai; nguyên liệu bị banish thay vì vào GY.', ['Crystron Citree','Crystron Sulfefnir','F.A. Dawn Dragster'])],end=['F.A. Dawn Dragster'],board='Dawn Dragster trong lượt đối thủ nếu Citree và Sulfefnir còn hợp lệ; có negate Spell/Trap bằng giảm Level.')
change('Gem-Knights',steps=[
 ('Normal Summon Nepyrim, tìm Gem-Knight Fusion.', ['Gem-Knight Nepyrim','Gem-Knight Fusion']),
 ('Nepyrim cho Normal Summon Gem-Armadillo; Armadillo tìm Quartz.', ['Gem-Knight Nepyrim','Gem-Armadillo','Gem-Knight Quartz']),
 ('Link Nepyrim và Gem-Armadillo thành Phantom Quartz; khi Link Summon tìm Gem-Knight Dispersion.', ['Gem-Knight Nepyrim','Gem-Armadillo','Gem-Knight Phantom Quartz','Gem-Knight Dispersion'])],end=['Gem-Knight Phantom Quartz'],board='Phantom Quartz, Fusion/Quartz/Dispersion trên tay và hai Gem trong GY; tiếp tục Fusion theo nguyên liệu hợp lệ.')
