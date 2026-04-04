import 'package:flutter/material.dart';
import 'package:capitalsense/service/api_service.dart';

class AdminProfileScreen extends StatefulWidget {
  const AdminProfileScreen({super.key});

  @override
  State<AdminProfileScreen> createState() => _AdminProfileScreenState();
}

class _AdminProfileScreenState extends State<AdminProfileScreen> {
  final ApiService _apiService = ApiService();
  bool _isLoggingOut = false;
  bool _isLoading = true;
  Map<String, dynamic>? _profile;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchProfile();
  }

  Future<void> _fetchProfile() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });
    try {
      final profile = await _apiService.getProfile();
      setState(() {
        _profile = profile;
        _isLoading = false;
      });
    } catch (e) {
      debugPrint("Profile fetch error: $e");
      setState(() {
        _isLoading = false;
        _errorMessage = e.toString().replaceAll('Exception: ', '');
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load profile: $_errorMessage')),
        );
      }
    }
  }

  Future<void> _logout() async {
    setState(() => _isLoggingOut = true);
    try {
      await _apiService.logout();
      if (mounted) {
        Navigator.pushNamedAndRemoveUntil(context, '/', (route) => false);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Logout failed: $e'), backgroundColor: Colors.red),
        );
      }
    } finally {
      if (mounted) setState(() => _isLoggingOut = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildProfileHeader(),
        Expanded(
          child: Container(
            width: double.infinity,
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.94),
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(35),
                topRight: Radius.circular(35),
              ),
            ),
            child: _isLoading 
                ? const Center(child: CircularProgressIndicator(color: Color(0xFF0F5B44)))
                : _errorMessage != null 
                    ? _buildErrorView()
                    : _buildProfileView(),
          ),
        ),
      ],
    );
  }

  Widget _buildProfileHeader() {
    return SafeArea(
      bottom: false,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 25, vertical: 30),
        child: Row(
          children: [
            CircleAvatar(
              radius: 35,
              backgroundColor: Colors.white24,
              child: const Icon(Icons.person, size: 40, color: Colors.white),
            ),
            const SizedBox(width: 20),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(_profile?['full_name'] ?? "Finance Manager", style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                Text(_profile?['business_name'] ?? "Business Owner", style: const TextStyle(color: Colors.white70, fontSize: 14)),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildErrorView() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(40),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline, color: Colors.red, size: 40),
            const SizedBox(height: 20),
            Text(_errorMessage ?? "Something went wrong", textAlign: TextAlign.center, style: const TextStyle(color: Colors.black54)),
            const SizedBox(height: 25),
            ElevatedButton(
              onPressed: _fetchProfile,
              child: const Text("Retry Fetching Profile"),
            ),
            TextButton(
              onPressed: _logout,
              child: const Text("Cancel & Logout", style: TextStyle(color: Colors.red)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProfileView() {
    return Column(
      children: [
        Expanded(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(30),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text("Registration Profile", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0B3B2E))),
                const SizedBox(height: 20),
                _buildInfoTile("Business Name", _profile?['business_name'] ?? "Not Found", Icons.business),
                _buildInfoTile("Registered Email", _profile?['email'] ?? "Not Found", Icons.email),
                _buildInfoTile("Office Address", _profile?['office_address'] ?? "Not Provided", Icons.location_on),
              ],
            ),
          ),
        ),
        _buildBottomLogoutAction(),
      ],
    );
  }

  Widget _buildBottomLogoutAction() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 30, vertical: 25),
      child: SafeArea(
        top: false,
        child: SizedBox(
          width: double.infinity,
          height: 55,
          child: OutlinedButton(
            style: OutlinedButton.styleFrom(
              side: const BorderSide(color: Colors.red, width: 2),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
            ),
            onPressed: _isLoggingOut ? null : _logout,
            child: _isLoggingOut
                ? const CircularProgressIndicator(color: Colors.red)
                : const Text(
                    "LOGOUT",
                    style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold, letterSpacing: 1.2),
                  ),
          ),
        ),
      ),
    );
  }

  Widget _buildInfoTile(String label, String value, IconData icon) {
    return Container(
      margin: const EdgeInsets.only(bottom: 15),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.grey.shade100),
      ),
      child: Row(
        children: [
          Icon(icon, color: const Color(0xFF0F5B44), size: 18),
          const SizedBox(width: 15),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: Colors.black54)),
                const SizedBox(height: 4),
                Text(value, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: Colors.black)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
