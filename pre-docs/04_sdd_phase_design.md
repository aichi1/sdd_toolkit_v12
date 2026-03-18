# AtCoder 学習教材セット — SDDフェーズ設計

## 概要

本ドキュメントは、AtCoder学習教材セットの **Spec-Driven Development (SDD) フェーズ設計** を定義する。
このpre-docsを使って `/init-task` → `/run-phase` を実行すると、
weekごとの教材（lecture.md + practice.md）が自動生成される。

---

## フェーズ構成

| SDD Phase | 対応Week | 内容 | 生成ファイル数 |
|-----------|---------|------|--------------|
| Phase 1 | Week 1-2 | 基礎固め（全探索・二分探索・累積和） | 4ファイル |
| Phase 2 | Week 3-6 | DP + グラフ基礎 | 8ファイル |
| Phase 3 | Week 7-10 | 中級テクニック（DFS・最短路・木DP・文字列） | 8ファイル |
| Phase 4 | Week 11-18 | 高度DP + データ構造（Union-Find・セグ木・BIT） | 16ファイル |
| Phase 5 | Week 19-24 | 水色到達演習・総合強化 | 12ファイル |

合計: **48ファイル**（lecture.md × 24 + practice.md × 24）

---

## 各フェーズの作業内容

### Phase 1: 基礎固め教材（Week 1-2）

**入力**: `02_curriculum_mapping.md` の Week 1-2 の仕様

**出力ファイル**:
```
outputs/phase-01/week-01/lecture.md    → 全探索・ブルートフォース
outputs/phase-01/week-01/practice.md   → ABC 灰〜茶前半問題 5問+
outputs/phase-01/week-02/lecture.md    → 二分探索・lower_bound
outputs/phase-01/week-02/practice.md   → ABC 灰〜茶問題 5問+
```

**品質チェックポイント**:
- [ ] C++ コードがコンパイル可能か（`g++ -std=c++17` で確認）
- [ ] ABC問題番号が実在するか（捏造していないか）
- [ ] difficulty 値が Week 1-2 の範囲（300〜600）に収まっているか
- [ ] 解説が初心者（茶色下位）にもわかるレベルか
- [ ] ヒントが3段階になっているか

---

### Phase 2: DP + グラフ基礎（Week 3-6）

**入力**: `02_curriculum_mapping.md` の Week 3-6 の仕様

**出力ファイル**:
```
outputs/phase-02/week-03/lecture.md    → 累積和・いもす法
outputs/phase-02/week-03/practice.md
outputs/phase-02/week-04/lecture.md    → DP入門（1次元DP）
outputs/phase-02/week-04/practice.md
outputs/phase-02/week-05/lecture.md    → DP応用（2次元・区間DP）
outputs/phase-02/week-05/practice.md
outputs/phase-02/week-06/lecture.md    → グラフ基礎・BFS
outputs/phase-02/week-06/practice.md
```

**品質チェックポイント**:
- [ ] DP の状態遷移が明確に説明されているか
- [ ] BFS の実装が queue を正しく使っているか
- [ ] difficulty が Week 3-6 の範囲（400〜800）に収まっているか

---

### Phase 3: 中級テクニック（Week 7-10）

**入力**: `02_curriculum_mapping.md` の Week 7-10 の仕様

**出力ファイル**:
```
outputs/phase-03/week-07/lecture.md    → DFS・連結成分
outputs/phase-03/week-07/practice.md
outputs/phase-03/week-08/lecture.md    → 最短路（ダイクストラ）
outputs/phase-03/week-08/practice.md
outputs/phase-03/week-09/lecture.md    → 木のDP・パス
outputs/phase-03/week-09/practice.md
outputs/phase-03/week-10/lecture.md    → 文字列（基本操作・ハッシュ）
outputs/phase-03/week-10/practice.md
```

**品質チェックポイント**:
- [ ] ダイクストラに priority_queue を使用しているか（O(E log V)）
- [ ] 木DPの再帰実装が正確か
- [ ] difficulty が Week 7-10 の範囲（600〜1000）に収まっているか

---

### Phase 4: 高度DP + データ構造（Week 11-18）

**入力**: `02_curriculum_mapping.md` の Week 11-18 の仕様

**出力ファイル**:
```
outputs/phase-04/week-11/lecture.md    → 数学（素数・GCD・mod）
outputs/phase-04/week-11/practice.md
outputs/phase-04/week-12/lecture.md    → bit全探索・bitmask DP
outputs/phase-04/week-12/practice.md
outputs/phase-04/week-13/lecture.md    → Union-Find
outputs/phase-04/week-13/practice.md
outputs/phase-04/week-14/lecture.md    → セグメント木（基礎）
outputs/phase-04/week-14/practice.md
outputs/phase-04/week-15/lecture.md    → BIT（Binary Indexed Tree）
outputs/phase-04/week-15/practice.md
outputs/phase-04/week-16/lecture.md    → 典型90問 前半精選
outputs/phase-04/week-16/practice.md
outputs/phase-04/week-17/lecture.md    → 最小全域木（クラスカル）
outputs/phase-04/week-17/practice.md
outputs/phase-04/week-18/lecture.md    → 二部グラフ・マッチング入門
outputs/phase-04/week-18/practice.md
```

**品質チェックポイント**:
- [ ] セグメント木の実装が正確か（区間クエリ・点更新）
- [ ] Union-Find の path compression が実装されているか
- [ ] difficulty が Week 11-18 の範囲（700〜1200）に収まっているか

---

### Phase 5: 水色到達演習（Week 19-24）

**入力**: `02_curriculum_mapping.md` の Week 19-24 の仕様

**出力ファイル**:
```
outputs/phase-05/week-19/lecture.md    → 典型90問 後半精選
outputs/phase-05/week-19/practice.md
outputs/phase-05/week-20/lecture.md    → ABC E/F 問題対策
outputs/phase-05/week-20/practice.md
outputs/phase-05/week-21/lecture.md    → 応用DP（桁DP・確率DP）
outputs/phase-05/week-21/practice.md
outputs/phase-05/week-22/lecture.md    → 幾何基礎（ベクトル・内積）
outputs/phase-05/week-22/practice.md
outputs/phase-05/week-23/lecture.md    → 総合演習 バーチャルコンテスト
outputs/phase-05/week-23/practice.md
outputs/phase-05/week-24/lecture.md    → 緑安定化・弱点集中補強
outputs/phase-05/week-24/practice.md
```

**品質チェックポイント**:
- [ ] difficulty が Week 19-24 の範囲（1000〜1400）に収まっているか
- [ ] 緑安定化に向けた戦略的な問題選択か
- [ ] ABC E/F レベルの解説が詳細か

---

## /run-phase の実行イメージ

```bash
# Phase 1 実行 → Week 1-2 の lecture.md + practice.md を生成（4ファイル）
/run-phase 1

# Phase 2 実行 → Week 3-6 の lecture.md + practice.md を生成（8ファイル）
/run-phase 2

# Phase 3 実行 → Week 7-10 の lecture.md + practice.md を生成（8ファイル）
/run-phase 3

# Phase 4 実行 → Week 11-18 の lecture.md + practice.md を生成（16ファイル）
/run-phase 4

# Phase 5 実行 → Week 19-24 の lecture.md + practice.md を生成（12ファイル）
/run-phase 5
```

---

## バッチ処理プロトコル（大規模生成時）

Phase 4以降は生成ファイル数が多いため、バッチ処理プロトコルに従う:

```
① Phase設計確認 → 家老レビュー → フィードバック反映
② Week-01のみ生成 → 殿QC
③ QC NG → 全停止 → 根本原因分析 → 修正 → ②に戻る
④ QC OK → 残りWeekを一括生成
⑤ Phase完了 → 最終QC
⑥ QC OK → 次Phaseへ（①に戻る）
```

**バッチサイズ上限**: 4週/セッション（Week単位でリセット可能）

---

## 注意事項

1. **教材特化SDD**: これは「教材作成」専用のSDD（CLIツール開発ではない）
2. **殿が実際に読む教材**: lecture.md は丁寧な解説が必須（読んで理解できること）
3. **ABC問題番号**: 実在するもののみ記載（捏造禁止）
4. **ヒントの段階性**: practice.md のヒントは必ず3段階（いきなりネタバレしない）
5. **カリキュラムの連続性**: 前Weekの知識を踏まえた積み上げ設計

---

## フェーズ間の依存関係

```
Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
  (独立)    (前Phaseの基礎知識を前提)
```

各Phaseは前Phaseの完了後に実行する（並列実行不可）。
ただし同一Phase内のWeek間では、lecture.md と practice.md を同時生成可能。

---

*作成: subtask_062a3 (ashigaru3) | 2026-03-19*
*参照: 01_requirements.md, 03_tech_constraints.md*
