import 'package:flutter/material.dart';
import 'package:capitalsense/service/api_service.dart';

class StrategyTab extends StatefulWidget {
  final Map<String, dynamic>? dashboardData;
  const StrategyTab({super.key, this.dashboardData});

  @override
  State<StrategyTab> createState() => _StrategyTabState();
}

class _StrategyTabState extends State<StrategyTab> with SingleTickerProviderStateMixin {
  final ApiService _api = ApiService();
  late TabController _tabCtrl;

  // Simulation state
  bool _isSimulating = false;
  Map<String, dynamic>? _simResult;
  final _balanceCtrl = TextEditingController();
  String _riskLevel = "MODERATE";

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    _balanceCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildHeader(),
        Expanded(
          child: Container(
            width: double.infinity,
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.94),
              borderRadius: const BorderRadius.only(topLeft: Radius.circular(35), topRight: Radius.circular(35)),
            ),
            child: Column(
              children: [
                const SizedBox(height: 8),
                _buildTabBar(),
                Expanded(
                  child: TabBarView(
                    controller: _tabCtrl,
                    children: [
                      _buildStrategiesView(),
                      _buildSimulationView(),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildHeader() {
    return SafeArea(
      bottom: false,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 20),
        child: Row(children: const [
          Icon(Icons.analytics, color: Colors.white, size: 26),
          SizedBox(width: 12),
          Text("Strategy & Simulations", style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
        ]),
      ),
    );
  }

  Widget _buildTabBar() {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 25),
      decoration: BoxDecoration(
        color: Colors.grey.shade100,
        borderRadius: BorderRadius.circular(16),
      ),
      child: TabBar(
        controller: _tabCtrl,
        indicator: BoxDecoration(
          color: const Color(0xFF0F5B44),
          borderRadius: BorderRadius.circular(14),
        ),
        labelColor: Colors.white,
        unselectedLabelColor: Colors.black54,
        labelStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
        tabs: const [
          Tab(text: "Payment Strategies"),
          Tab(text: "What-If Simulator"),
        ],
      ),
    );
  }

  // ══════════════════════════════════════════════════════════════════════════
  // STRATEGIES VIEW
  // ══════════════════════════════════════════════════════════════════════════

  Widget _buildStrategiesView() {
    final decisions = widget.dashboardData?['decisions'];
    if (decisions == null) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(40),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.query_stats, size: 45, color: Colors.grey),
              SizedBox(height: 16),
              Text("No strategy data yet", style: TextStyle(color: Colors.black87, fontWeight: FontWeight.bold, fontSize: 16)),
              SizedBox(height: 8),
              Text("Add your invoices and expenses to generate AI strategies", textAlign: TextAlign.center, style: TextStyle(color: Colors.black45, fontSize: 13)),
            ],
          ),
        ),
      );
    }

    final overall = decisions['overall_recommendation'] ?? '';
    final base = decisions['base_case'];
    final strategy = (base?['recommended_strategy'] as String?)?.toUpperCase() ?? 'BALANCED';

    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 25),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ── Strategic Summary Row ──────────────────────────────────────────
          Row(
            children: [
              Expanded(child: _buildStrategyMetric("RECOMMENDED", strategy, Icons.star, const Color(0xFF0B3B2E))),
              const SizedBox(width: 12),
              Expanded(child: _buildStrategyMetric("SCENARIOS", "3 PROJECTIONS", Icons.layers, Colors.blue.shade700)),
            ],
          ),
          const SizedBox(height: 25),
          
          _buildAIInsightCard(overall),
          const SizedBox(height: 30),
          
          Text("DETAILED SCENARIOS", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.black45, letterSpacing: 1.2)),
          const SizedBox(height: 16),
          
          _buildScenarioSection("BASE CASE", decisions['base_case'], const Color(0xFF0F5B44)),
          const SizedBox(height: 16),
          _buildScenarioSection("BEST CASE", decisions['best_case'], Colors.blue.shade700),
          const SizedBox(height: 16),
          _buildScenarioSection("WORST CASE", decisions['worst_case'], Colors.red.shade700),
          
          const SizedBox(height: 120),
        ],
      ),
    );
  }

  Widget _buildStrategyMetric(String label, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [BoxShadow(color: color.withOpacity(0.08), blurRadius: 10, offset: const Offset(0, 4))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, size: 14, color: color),
              const SizedBox(width: 6),
              Text(label, style: const TextStyle(fontSize: 9, fontWeight: FontWeight.bold, color: Colors.black45)),
            ],
          ),
          const SizedBox(height: 8),
          Text(value, style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: color)),
        ],
      ),
    );
  }

  Widget _buildAIInsightCard(String text) {
    if (text.isEmpty) return const SizedBox.shrink();
    
    // Simplistic formatting for AI text
    final lines = text.split('\n').where((l) => l.trim().isNotEmpty && !l.contains('===')).toList();
    
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(22),
      decoration: BoxDecoration(
        color: const Color(0xFF0B3B2E),
        borderRadius: BorderRadius.circular(25),
        boxShadow: [BoxShadow(color: const Color(0xFF0B3B2E).withOpacity(0.2), blurRadius: 15, offset: const Offset(0, 8))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.lightbulb, color: Color(0xFF1B7A5A), size: 24),
              SizedBox(width: 12),
              Text("Strategic Insight", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
            ],
          ),
          const SizedBox(height: 16),
          ...lines.take(6).map((line) => Padding(
                padding: const EdgeInsets.only(bottom: 10),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("•", style: TextStyle(color: Color(0xFF1B7A5A), fontSize: 18)),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        line.trim(),
                        style: const TextStyle(fontSize: 13, color: Colors.white70, height: 1.5),
                      ),
                    ),
                  ],
                ),
              )),
        ],
      ),
    );
  }

  Widget _buildScenarioSection(String title, Map<String, dynamic>? data, Color color) {
    if (data == null) return const SizedBox.shrink();

    final recommended = data['recommended_strategy'] ?? '';
    final reasoning = data['reasoning'] ?? '';
    final balanced = data['balanced'] as Map<String, dynamic>? ?? {};
    final survival = (balanced['survival_probability'] as num?)?.toDouble() ?? 0;
    final cashAfter = (balanced['estimated_cash_after'] as num?)?.toDouble() ?? 0;

    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(22),
        color: Colors.white,
        boxShadow: [BoxShadow(color: color.withOpacity(0.05), blurRadius: 12, offset: const Offset(0, 4))],
      ),
      child: Theme(
        data: Theme.of(context).copyWith(dividerColor: Colors.transparent),
        child: ExpansionTile(
          tilePadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
          childrenPadding: const EdgeInsets.fromLTRB(20, 0, 20, 20),
          leading: Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(15)),
            child: Icon(Icons.show_chart, color: color, size: 22),
          ),
          title: Text(title, style: TextStyle(fontWeight: FontWeight.bold, color: color, fontSize: 15, letterSpacing: 0.5)),
          subtitle: Padding(
            padding: const EdgeInsets.only(top: 6),
            child: Row(
              children: [
                _buildScenarioPill(recommended, color),
                const SizedBox(width: 12),
                _buildScenarioPill("${survival.toStringAsFixed(0)}% Odds", survival >= 70 ? const Color(0xFF0F5B44) : Colors.orange),
                const SizedBox(width: 12),
                Text(_formatCurrency(cashAfter), style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: Colors.black45)),
              ],
            ),
          ),
          initiallyExpanded: title == "BASE CASE",
          children: [
            const Divider(),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(color: Colors.grey.shade50, borderRadius: BorderRadius.circular(15)),
              child: Text(reasoning, style: const TextStyle(fontSize: 12, color: Colors.black54, height: 1.5)),
            ),
            const SizedBox(height: 16),
            _buildStrategyComparison(data, color),
          ],
        ),
      ),
    );
  }

  Widget _buildScenarioPill(String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
      child: Text(text.toUpperCase(), style: TextStyle(fontSize: 9, fontWeight: FontWeight.bold, color: color)),
    );
  }

  Widget _buildStrategyComparison(Map<String, dynamic> scenario, Color baseColor) {
    final strategies = [
      {"key": "aggressive", "label": "Aggressive", "icon": Icons.flash_on, "color": Colors.red.shade600},
      {"key": "balanced", "label": "Balanced", "icon": Icons.balance, "color": const Color(0xFF0F5B44)},
      {"key": "conservative", "label": "Conservative", "icon": Icons.shield, "color": Colors.blue.shade700},
    ];

    final recommended = (scenario['recommended_strategy'] ?? '').toString().toUpperCase();

    return Column(
      children: strategies.map((s) {
        final data = scenario[s['key']] as Map<String, dynamic>?;
        if (data == null) return const SizedBox.shrink();
        final isRecommended = (s['label'] as String).toUpperCase() == recommended;

        final totalPay = (data['total_payment'] as num?)?.toDouble() ?? 0;
        final penalty = (data['total_penalty_cost'] as num?)?.toDouble() ?? 0;
        final cashAfter = (data['estimated_cash_after'] as num?)?.toDouble() ?? 0;
        final survival = (data['survival_probability'] as num?)?.toDouble() ?? 0;
        final decisions = data['decisions'] as List? ?? [];

        return Container(
          margin: const EdgeInsets.only(bottom: 10),
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            color: isRecommended ? (s['color'] as Color).withOpacity(0.04) : Colors.grey.shade50,
            border: Border.all(color: isRecommended ? (s['color'] as Color).withOpacity(0.3) : Colors.grey.shade200),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(s['icon'] as IconData, size: 16, color: s['color'] as Color),
                  const SizedBox(width: 6),
                  Text(s['label'] as String, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: s['color'] as Color)),
                  if (isRecommended) ...[
                    const SizedBox(width: 8),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                      decoration: BoxDecoration(color: (s['color'] as Color).withOpacity(0.15), borderRadius: BorderRadius.circular(6)),
                      child: const Text("★ PICK", style: TextStyle(fontSize: 8, fontWeight: FontWeight.bold)),
                    ),
                  ],
                ],
              ),
              const SizedBox(height: 10),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  _buildStratStat("Pay", _formatCurrency(totalPay), s['color'] as Color),
                  _buildStratStat("Penalty", _formatCurrency(penalty), penalty > 0 ? Colors.red : Colors.green),
                  _buildStratStat("Cash After", _formatCurrency(cashAfter), const Color(0xFF0F5B44)),
                  _buildStratStat("Survival", "${survival.toStringAsFixed(0)}%", survival >= 80 ? Colors.green : Colors.orange),
                ],
              ),
              if (decisions.isNotEmpty) ...[
                const SizedBox(height: 10),
                const Divider(height: 1),
                const SizedBox(height: 8),
                ...decisions.map((d) => _buildDecisionItem(d)),
              ],
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildStratStat(String label, String value, Color color) {
    return Column(
      children: [
        Text(value, style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: color)),
        Text(label, style: const TextStyle(fontSize: 8, color: Colors.black38)),
      ],
    );
  }

  Widget _buildDecisionItem(Map<String, dynamic> d) {
    final status = d['status']?.toString() ?? '';
    final payAmount = (d['pay_amount'] as num?)?.toDouble() ?? 0;
    final vendorName = d['vendor_name'] ?? d['obligation_id'] ?? '';
    final rationale = d['rationale'] ?? '';
    final delayDays = d['delay_days'] as int? ?? 0;

    Color statusColor;
    IconData statusIcon;
    switch (status) {
      case 'PAY_IN_FULL':
        statusColor = Colors.green;
        statusIcon = Icons.check_circle;
        break;
      case 'PARTIAL_PAY':
        statusColor = Colors.orange;
        statusIcon = Icons.timelapse;
        break;
      case 'DELAY':
        statusColor = Colors.red.shade400;
        statusIcon = Icons.schedule;
        break;
      case 'STRATEGIC_DEFAULT':
        statusColor = Colors.red;
        statusIcon = Icons.block;
        break;
      default:
        statusColor = Colors.grey;
        statusIcon = Icons.help;
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 6),
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: statusColor.withOpacity(0.04),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: statusColor.withOpacity(0.15)),
      ),
      child: Row(
        children: [
          Icon(statusIcon, size: 16, color: statusColor),
          const SizedBox(width: 8),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(vendorName, style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 11)),
                Text(
                  "${status.replaceAll('_', ' ')}${delayDays > 0 ? ' (+$delayDays days)' : ''} • $rationale",
                  style: TextStyle(fontSize: 9, color: statusColor, height: 1.3),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
          Text(_formatCurrency(payAmount), style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: statusColor)),
        ],
      ),
    );
  }

  // ══════════════════════════════════════════════════════════════════════════
  // SIMULATION VIEW
  // ══════════════════════════════════════════════════════════════════════════

  Widget _buildSimulationView() {
    return SingleChildScrollView(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 25),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildSimulationForm(),
          const SizedBox(height: 30),
          if (_isSimulating) 
            const Center(
              child: Padding(
                padding: EdgeInsets.all(40), 
                child: CircularProgressIndicator(color: Color(0xFF0F5B44))
              )
            ),
          if (_simResult != null && !_isSimulating) ...[
            Text("DETAILED PROJECTION", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.black45, letterSpacing: 1.2)),
            const SizedBox(height: 16),
            _buildSimulationResults(),
          ],
          const SizedBox(height: 120),
        ],
      ),
    );
  }

  Widget _buildSimulationForm() {
    return Container(
      padding: const EdgeInsets.all(25),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(25),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 15, offset: const Offset(0, 4))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(color: const Color(0xFF0F5B44).withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
                child: const Icon(Icons.psychology, color: Color(0xFF0F5B44), size: 24),
              ),
              const SizedBox(width: 15),
              const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("What-If Scenario", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF0B3B2E))),
                  Text("Test liquidity across risk appetites", style: TextStyle(fontSize: 11, color: Colors.black45)),
                ],
              ),
            ],
          ),
          const SizedBox(height: 25),
          TextField(
            controller: _balanceCtrl,
            keyboardType: TextInputType.number,
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            decoration: InputDecoration(
              labelText: "Simulation Balance (₹)",
              hintText: "Enter amount to test",
              floatingLabelBehavior: FloatingLabelBehavior.always,
              prefixIcon: const Icon(Icons.account_balance_wallet, color: Color(0xFF0F5B44), size: 20),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(18), borderSide: BorderSide(color: Colors.grey.shade300)),
              enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(18), borderSide: BorderSide(color: Colors.grey.shade200)),
              filled: true,
              fillColor: Colors.grey.shade50,
            ),
          ),
          const SizedBox(height: 20),
          const Text("Risk Strategy Level", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.black54, letterSpacing: 0.5)),
          const SizedBox(height: 12),
          Row(
            children: ["AGGRESSIVE", "MODERATE", "CONSERVATIVE"].map((level) {
              final isSelected = _riskLevel == level;
              Color chipColor;
              switch (level) {
                case "AGGRESSIVE": chipColor = Colors.red.shade700; break;
                case "CONSERVATIVE": chipColor = Colors.blue.shade700; break;
                default: chipColor = const Color(0xFF0F5B44);
              }
              return Expanded(
                child: GestureDetector(
                  onTap: () => setState(() => _riskLevel = level),
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 200),
                    margin: const EdgeInsets.symmetric(horizontal: 4),
                    padding: const EdgeInsets.symmetric(vertical: 12),
                    decoration: BoxDecoration(
                      color: isSelected ? chipColor : Colors.white,
                      borderRadius: BorderRadius.circular(15),
                      border: Border.all(color: isSelected ? chipColor : Colors.grey.shade200),
                      boxShadow: isSelected ? [BoxShadow(color: chipColor.withOpacity(0.3), blurRadius: 8, offset: const Offset(0, 3))] : [],
                    ),
                    child: Center(
                      child: Text(
                        level,
                        style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: isSelected ? Colors.white : Colors.black45),
                      ),
                    ),
                  ),
                ),
              );
            }).toList(),
          ),
          const SizedBox(height: 25),
          SizedBox(
            width: double.infinity,
            height: 55,
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF0F5B44),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
                elevation: 4, shadowColor: const Color(0xFF0F5B44).withOpacity(0.4),
              ),
              onPressed: _isSimulating ? null : _runSimulation,
              child: const Text("RUN SIMULATION", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, letterSpacing: 1.2)),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _runSimulation() async {
    setState(() {
      _isSimulating = true;
      _simResult = null;
    });
    try {
      final result = await _api.simulateScenario(
        balance: _balanceCtrl.text.isNotEmpty ? double.tryParse(_balanceCtrl.text) : null,
        riskLevel: _riskLevel,
      );
      if (mounted) setState(() => _simResult = result);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Simulation error: $e"), backgroundColor: Colors.red));
      }
    } finally {
      if (mounted) setState(() => _isSimulating = false);
    }
  }

  Widget _buildSimulationResults() {
    final healthScore = (_simResult?['health_score'] as num?)?.toInt() ?? 0;
    final runway = _simResult?['cash_runway_days'];
    final recommendation = _simResult?['recommendation'] ?? '';
    final overallRec = _simResult?['overall_recommendation'] ?? '';

    Color healthColor = healthScore >= 70
        ? const Color(0xFF0F5B44)
        : healthScore >= 40 ? Colors.orange.shade800 : Colors.red.shade700;

    return Container(
      padding: const EdgeInsets.all(25),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(30),
        boxShadow: [BoxShadow(color: healthColor.withOpacity(0.1), blurRadius: 20, offset: const Offset(0, 6))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text("Simulated Health", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 17, color: Color(0xFF0B3B2E))),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(color: healthColor.withOpacity(0.1), borderRadius: BorderRadius.circular(20)),
                child: Text("$healthScore / 100", style: TextStyle(fontWeight: FontWeight.bold, color: healthColor, fontSize: 13)),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              Expanded(
                child: _buildSimMetricCard("CASH RUNWAY", runway != null ? "$runway days" : "∞", Icons.timer, Colors.blue.shade700),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _buildSimMetricCard("STRATEGY", recommendation, Icons.psychology_outlined, const Color(0xFF0F5B44)),
              ),
            ],
          ),
          const SizedBox(height: 20),
          const Text("EXPLAINABILITY", style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.black38, letterSpacing: 1)),
          const SizedBox(height: 10),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(color: Colors.grey.shade50, borderRadius: BorderRadius.circular(20), border: Border.all(color: Colors.grey.shade100)),
            child: Text(
              overallRec,
              style: const TextStyle(fontSize: 12, color: Colors.black54, height: 1.6),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSimMetricCard(String label, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.05),
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: color.withOpacity(0.1)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 18),
          const SizedBox(height: 8),
          Text(value, style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: color), maxLines: 1, overflow: TextOverflow.ellipsis),
          const SizedBox(height: 2),
          Text(label, style: const TextStyle(fontSize: 8, fontWeight: FontWeight.bold, color: Colors.black38)),
        ],
      ),
    );
  }

  String _formatCurrency(double amount) {
    if (amount >= 10000000) return "₹${(amount / 10000000).toStringAsFixed(1)}Cr";
    if (amount >= 100000) return "₹${(amount / 100000).toStringAsFixed(1)}L";
    if (amount >= 1000) return "₹${(amount / 1000).toStringAsFixed(1)}K";
    return "₹${amount.toStringAsFixed(0)}";
  }
}
